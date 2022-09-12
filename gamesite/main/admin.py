from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe
from main.models import News, CategoryNews, Comment, CinemaComment, CinemaNews, Games, GamesCategory, GamesComment, \
    NewsImage, CinemaImage, GamesImage


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ['title', 'created', 'available', 'category', 'get_photo']
    list_filter = ['available', 'created']
    list_editable = ['available']
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True
    save_as = True

    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url }" width="50">')
        return '-'

    get_photo.short_description = 'Mark'

@admin.register(CategoryNews)
class CategoryNewsAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


class CinemaAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = CinemaNews
        fields = '__all__'

@admin.register(CinemaNews)
class CinemaNewsAdmin(admin.ModelAdmin):
    form =CinemaAdminForm
    list_display = ['title', 'created', 'available', 'get_photo']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['available']
    search_fields = ['title']
    save_on_top = True
    save_as = True
    prepopulated_fields = {'slug': ('title',)}


    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url }" width="50">')
        return '-'

class GamesAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Games
        fields = '__all__'

@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    form = GamesAdminForm
    list_display = ['title', 'created', 'available', 'get_photo']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['available']
    search_fields = ['title']
    save_on_top = True
    save_as = True
    prepopulated_fields = {'slug': ('title',)}

    def get_photo(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url }" width="50">')
        return '-'


@admin.register(GamesCategory)
class GamesCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Comment)
admin.site.register(CinemaComment)
admin.site.register(GamesComment)
admin.site.register(NewsImage)
admin.site.register(CinemaImage)
admin.site.register(GamesImage)

