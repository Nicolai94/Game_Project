from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from shop.views import HomeView, ProductDetailView, CustomLoginView, RegisterView, CustomLogoutView, \
    CustomProfileView, AddToCartView, MyCartView, CheckoutView, ManageCartView, EmptyCartView, AddCommentProduct, \
    PasswordForgotView, PasswordResetView, CustomOrderDetailView, AdminLoginView, AdminHomeView, AdminOrderDetailView, \
    AdminOrderListView, AdminOrderStatusChangeView, AdminProductListView, AdminProductCreateView, \
    AdminProductDeleteView, AdminProductUpdateView


urlpatterns = [
    path('', HomeView.as_view(), name='shop_home'),
    path('/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', CustomProfileView.as_view(), name='profile'),
    path('profile/order<int:pk>/', CustomOrderDetailView.as_view(), name='orderdetail'),
    path('add-to-cart-<int:pro_id>/', AddToCartView.as_view(), name='add_to_cart'),
    path('my-cart/', MyCartView.as_view(), name='mycart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('manage-carts/<int:cp_id>/', ManageCartView.as_view(), name='managecart'),
    path('empty-cart/', EmptyCartView.as_view(), name='emptycart'),
    path('comment-product/<int:pk>/', AddCommentProduct.as_view(), name='comment_product'),
    path('forgot-password/', PasswordForgotView.as_view(), name='passwordforgot'),
    path('/password-reset/<email>/<token>/', PasswordResetView.as_view(), name='passwordreset'),
    #admin pages
    path('admin-login/', AdminLoginView.as_view(), name='adminlogin'),
    path('admin-home/', AdminHomeView.as_view(), name='adminhome'),
    path('admin-order/<int:pk>/', AdminOrderDetailView.as_view(), name='adminorderdetail'),
    path('admin-order/<int:pk>/', AdminOrderDetailView.as_view(), name='adminorderdetail'),
    path('admin-all-orders/', AdminOrderListView.as_view(), name='adminorderlist'),
    path('admin-order-<int:pk>-change/', AdminOrderStatusChangeView.as_view(), name='adminorderstatuschange'),
    path('admin-product/list/', AdminProductListView.as_view(), name='adminproductlist'),
    path('admin-product/add/', AdminProductCreateView.as_view(), name='adminproductcreate'),
    path('delete-product/<str:slug>/', AdminProductDeleteView.as_view(), name='delete_products'),
    path('update-product/<str:slug>/', AdminProductUpdateView.as_view(), name='update_products'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)