from django import forms

from main.models import Comment, CinemaComment, GamesComment, News, Games, CinemaNews


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'content')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'email': forms.TextInput(attrs={'class': 'col-sm-12'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class CinemaCommentForm(forms.ModelForm):
    class Meta:
        model = CinemaComment
        fields = ('name', 'email', 'content')


class GamesCommentForm(forms.ModelForm):
    class Meta:
        model = GamesComment
        fields = ('name', 'email', 'content')


class NewsForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
                'class': 'form-control',
                'multiple': True
            }))

    class Meta:
        model = News
        fields = ['title', 'slug', 'category', 'image', 'available', 'content']
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
                'class': 'form-control'
            }),
            'available': forms.CheckboxInput(),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write description here',
                'rows': 5
            }),
        }


class GamesForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
                'class': 'form-control',
                'multiple': True
            }))

    class Meta:
        model = Games
        fields = ['title', 'slug', 'category', 'image', 'video', 'available', 'content']
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
                'class': 'form-control'
            }),
            'available': forms.CheckboxInput(),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write description here',
                'rows': 5
            }),
            'video': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


class CinemaForm(forms.ModelForm):
    more_images = forms.FileField(required=False, widget=forms.FileInput(attrs={
                'class': 'form-control',
                'multiple': True
            }))

    class Meta:
        model = CinemaNews
        fields = ['title', 'slug', 'image', 'available', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the product title here...'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter the product slug here...'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
            'available': forms.CheckboxInput(),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write description here',
                'rows': 5
            }),
        }
