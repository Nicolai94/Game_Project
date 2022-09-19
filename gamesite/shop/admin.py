from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from shop.models import Product, Category, ProductComment, Order, Customer, Cart, CartProduct, Admin, ProductImage


class ProductAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget())
    minimal_requirements = forms.CharField(widget=CKEditorUploadingWidget())
    normal_requirements = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('title', 'slug', 'category', 'price', 'view_count', 'get_photo')
    list_filter = ['category', 'price']
    list_editable = ['price']
    search_fields = ['title']
    prepopulated_fields = {'slug':('title',)}
    save_on_top = True

    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url }" width="50">')
        return '-'

    get_photo.short_description = 'Mark'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug':('title',)}


@admin.register(ProductComment)
class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'created']
    list_filter = ['name']
    save_as = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['cart', 'ordered_by', 'order_status', 'total']
    list_editable = ['order_status']

admin.site.register(Customer)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Admin)
admin.site.register(ProductImage)
