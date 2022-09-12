from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import TemplateView, FormView, CreateView, DetailView, ListView, DeleteView, UpdateView

from shop.models import Product, Customer, Cart, CartProduct, Order, Admin, ORDER_STATUS, ProductImage

from shop.forms import CustomLoginForm, RegisterForm, CheckoutForm, ProductCommentForm, PasswordForgotForm, \
    PasswordResetForm, ProductForm

from shop.utils import password_reset_token


class EcomMixin(object):
    def dispatch(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            if request.user.is_authenticated and request.user.customer:
                cart_obj.customer = request.user.customer
                cart_obj.save()
        return super().dispatch(request, *args, **kwargs)


class HomeView(EcomMixin, TemplateView):
    template_name = 'shop/shop_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_products = Product.objects.all().order_by('-id')
        paginator = Paginator(all_products, 1)
        page_number = self.request.GET.get('page')
        product_list = paginator.get_page(page_number)
        context['product_list'] = product_list
        return context


class ProductDetailView(EcomMixin, TemplateView):
    template_name = 'shop/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context


class RegisterView(CreateView):
    template_name = 'shop/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username, email, password)
        form.instance.user = user
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(FormView):
    template_name = 'shop/login.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        pword = form.cleaned_data.get('password')
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Customer.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Invalid credentials'})
        return super().form_valid(form)

    def get_success_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET('next')
            return next_url
        else:
            return self.success_url


class CustomLogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('shop_home')


class CustomProfileView(EcomMixin, TemplateView):
    template_name = 'shop/profile.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect('login/?next=/profile/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.request.user.customer
        print(customer)
        context['customer'] = customer
        orders = Order.objects.filter(cart__customer=customer).order_by('-id')
        print(orders)
        context['orders'] = orders
        return context


class CustomOrderDetailView(EcomMixin, DetailView):
    template_name = 'shop/orderdetail.html'
    model = Order
    context_object_name = 'ord_obj'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if request.user.is_authenticated and Customer.objects.filter(user=request.user).exists():
            order_id = self.kwargs['pk']
            order = Order.objects.get(id=order_id)
            if request.user.customer != order.cart.customer:
                return redirect('profile')
        else:
            return redirect('login/?next=/profile/')
        return super().dispatch(request, *args, **kwargs)


class ManageCartView(EcomMixin, View):

    def get(self, request, *args, **kwargs):
        cp_id = self.kwargs['cp_id']
        action = request.GET.get('action')
        cp_obj = CartProduct.objects.get(id=cp_id)
        cart_obj = cp_obj.cart
        if action == 'inc':
            cp_obj.quantity += 1
            cp_obj.subtotal += cp_obj.rate
            cp_obj.save()
            cart_obj.total += cp_obj.rate
            cart_obj.save()
        elif action == 'dcr':
            cp_obj.quantity -= 1
            cp_obj.subtotal -= cp_obj.rate
            cp_obj.save()
            cart_obj.total -= cp_obj.rate
            cart_obj.save()
            if cp_obj.quantity == 0:
                cp_obj.delete()
        elif action == 'rmv':
            cart_obj.total -= cp_obj.subtotal
            cart_obj.save()
            cp_obj.delete()
        return redirect('mycart')


class EmptyCartView(EcomMixin, View):

    def get(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
            cart.cartproduct_set.all().delete()
            cart.total = 0
            cart.save()
        return redirect('mycart')


class MyCartView(EcomMixin, TemplateView):
    template_name = 'shop/mycart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context['cart'] = cart
        return context


class AddToCartView(EcomMixin, TemplateView):
    template_name = "shop/add_to_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # get product id from requested url
        product_id = self.kwargs['pro_id']
        # get product
        product_obj = Product.objects.get(id=product_id)

        # check if cart exists
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product=product_obj)

            # item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.subtotal += product_obj.price
                cartproduct.save()
                cart_obj.total += product_obj.price
                cart_obj.save()
            # new item is added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1,
                    subtotal=product_obj.price)
                cart_obj.total += product_obj.price
                cart_obj.save()

        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                cart=cart_obj, product=product_obj, rate=product_obj.price, quantity=1,
                subtotal=product_obj.price)
            cart_obj.total += product_obj.price
            cart_obj.save()

        return context


class CheckoutView(EcomMixin, CreateView):
    template_name = 'shop/checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('shop_home')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if request.user.is_authenticated and request.user.customer:
            pass
        else:
            return redirect('login/?next=/checkout/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get('cart_id', None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
        else:
            cart_obj = None
        context['cart'] = cart_obj
        return context

    def form_valid(self, form):
        cart_id = self.request.session.get('cart_id')
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            form.instance.cart = cart_obj
            form.instance.subtotal = cart_obj.total
            form.instance.discount = 0
            form.instance.total = cart_obj.total
            form.instance.order_status = 'Order Received'
            del self.request.session['cart_id']
        else:
            return redirect('shop_home')
        return super().form_valid(form)


class AddCommentProduct(View):

    def post(self, request, pk):
        form = ProductCommentForm(request.POST)
        products = Product.objects.get(id=pk)
        if form.is_valid():
            ''' Stop save form'''
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.products = products
            form.save()
        return redirect(products.get_absolute_url())


class PasswordForgotView(FormView):
    template_name = 'shop/forgotpassword.html'
    form_class = PasswordForgotForm
    success_url = '/forgot-password/?m=s'

    def form_valid(self, form):
        # get email from user
        email = form.cleaned_data.get('email')
        # get current host ip/domain
        url = self.request.META['HTTP_HOST']
        # get customer and then user
        customer = Customer.objects.get(user__email=email)
        user = customer.user
        # send mail to the user with email
        text_content = 'Please Click the link below to reset your password'
        html_content = url + '/password-reset/' + email + '/' + password_reset_token.make_token(user) + '/'
        send_mail(
            'PasswordReset Link | Django Ecommerce',
            text_content + html_content,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return super().form_valid(form)


class PasswordResetView(FormView):
    template_name = 'passwordreset.html'
    form_class = PasswordResetForm
    success_url = '/login/'

    def dispatch(self, request, *args, **kwargs):
        email = self.kwargs.get('email')
        user = User.objects.get(email=email)
        token = self.kwargs.get('token')
        if user is None and password_reset_token.check_token(user, token):
            pass
        else:
            return redirect(reverse('passwordforgot')+ '?m=e')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['new_password']
        email = self.kwargs.get('email')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return super().form_valid(form)


    #Admin Pages


class AdminLoginView(FormView):
    template_name = 'adminpages/adminlogin.html'
    form_class = CustomLoginForm
    success_url = reverse_lazy('adminhome')

    def form_valid(self, form):
        uname = form.cleaned_data.get('username')
        pword = form.cleaned_data.get('password')
        usr = authenticate(username=uname, password=pword)
        if usr is not None and Admin.objects.filter(user=usr).exists():
            login(self.request, usr)
        else:
            return render(self.request, self.template_name, {'form': self.form_class, 'error': 'Invalid credentials'})
        return super().form_valid(form)


class AdminRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect('/admin-login/')
        return super().dispatch(request, *args, **kwargs)


class AdminHomeView(AdminRequiredMixin, TemplateView):
    template_name = 'adminpages/adminhome.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pendingorders'] = Order.objects.filter(order_status='Order Received').order_by('-id')
        return context


class AdminOrderDetailView(AdminRequiredMixin, DetailView):
    template_name = 'adminpages/adminorderdetail.html'
    model = Order
    context_object_name = 'ord_obj'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['allstatus'] = ORDER_STATUS
        return context


class AdminOrderListView(AdminRequiredMixin, ListView):
    template_name = 'adminpages/adminorderlist.html'
    queryset = Order.objects.all().order_by('-id')
    context_object_name = 'allorders'


class AdminOrderStatusChangeView(AdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['pk']
        order_obj = Order.objects.get(id=order_id)
        new_status = request.POST.get('status')
        order_obj.order_status = new_status
        order_obj.save()
        return redirect(reverse_lazy('adminorderdetail', kwargs={'pk': self.kwargs['pk']}))


class AdminProductListView(ListView):
    template_name = 'adminpages/adminproductlist.html'
    queryset = Product.objects.all().order_by('id')
    context_object_name = 'allproducts'


class AdminProductCreateView(AdminRequiredMixin, CreateView):
    template_name = 'adminpages/adminproductcreate.html'
    form_class = ProductForm
    success_url = reverse_lazy('adminproductlist')

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist('more_images')
        for i in images:
            ProductImage.objects.create(product=p, image=i)
        return super().form_valid(form)


class AdminProductDeleteView(DeleteView):
    model = Product
    template_name = 'adminpages/admin_confirm_delete.html'
    success_url = reverse_lazy('admincinemalist')


class AdminProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'adminpages/admin_update_form.html'
    success_url = '/shop/admin-cinema/list/'