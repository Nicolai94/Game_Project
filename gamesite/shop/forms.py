from django import forms
from .models import *


class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Customer
        fields = ['username', 'password', 'email', 'full_name', 'address']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
        }

        def clean_username(self):
            uname = self.cleaned_data.get('username')
            if User.objects.filter(username=uname).exists():
                raise forms.ValidationError(
                    'User with this username already exists.'
                )
            return uname


class CustomLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['ordered_by', 'shipping_address', 'mobile', 'email']


class ProductCommentForm(forms.ModelForm):
    class Meta:
        model = ProductComment
        fields = ('name', 'email', 'content')


class PasswordForgotForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter the email used in customer account',
    }))

    def clean_email(self):
        e = self.cleaned_data.get('email')
        if Customer.objects.filter(user__email=e).exists():
            pass
        else:
            raise forms.ValidationError('Customer with this account does not exists ..')
        return e


class PasswordResetForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Enter New Password'
    }), label='New Password')
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'autocomplete': 'new-password',
        'placeholder': 'Confirm New Password'
    }), label='Confirm New Password')

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                'New passwords did not match!'
            )
        return confirm_new_password


class ProductForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
                'class': 'form-control',
                'multiple': True
            }))

    class Meta:
        model = Product
        fields = ['title', 'slug', 'category', 'image', 'price', 'description', 'minimal_requirements',
                  'normal_requirements', 'video']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the product title here...'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the product slug here...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'multiple': True
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Price of the product'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write description here',
                'rows': 5
            }),
            'minimal_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Minimal requirements',
                'rows': 5
            }),
            'normal_requirements': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Normal requirements',
                'rows': 5
            }),
            'video': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }