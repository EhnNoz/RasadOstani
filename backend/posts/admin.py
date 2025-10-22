# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Channel, Platform, Province, NewsType, NewsTopic,
    Post, UserProvinceAccess, PoliticalCategory, UserCategory
)


class PoliticalCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_per_page = 20


class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_per_page = 20


class ChannelAdmin(admin.ModelAdmin):
    list_display = [
        'name_fa', 'username', 'channel_type',
        'get_political_category', 'get_user_category',
        'platform', 'created_at'
    ]
    list_filter = [
        'channel_type', 'platform', 'political_category',
        'user_category', 'created_at'
    ]
    search_fields = [
        'name_fa', 'username', 'political_category__name',
        'user_category__name', 'tag'
    ]
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 20

    def get_political_category(self, obj):
        return obj.political_category.name if obj.political_category else '-'

    get_political_category.short_description = 'دسته سیاسی'

    def get_user_category(self, obj):
        return obj.user_category.name if obj.user_category else '-'

    get_user_category.short_description = 'دسته کاربری'

    fieldsets = (
        ('اطلاعات پایه', {
            'fields': (
                'name_fa', 'username', 'user_id', 'channel_type',
                'platform'
            )
        }),
        ('دسته‌بندی‌ها', {
            'fields': (
                'political_category', 'user_category', 'sub_category', 'tag'
            )
        }),
        ('تاریخ‌ها', {
            'fields': (
                'created_at', 'updated_at'
            )
        }),
    )


class PlatformAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    list_per_page = 20


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name_fa', 'name_en']
    search_fields = ['name_fa', 'name_en']
    list_per_page = 20


class NewsTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'news_type_query']
    search_fields = ['name']
    list_per_page = 20


class NewsTopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'news_topic_query']
    search_fields = ['name']
    list_per_page = 20


class PostAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'platform', 'province', 'channel',
        'media_type', 'sentiment', 'like_count',
        'view_count', 'datetime_create'
    ]
    list_filter = [
        'platform', 'province', 'channel', 'media_type',
        'sentiment', 'npo', 'emo', 'datetime_create'
    ]
    search_fields = [
        'username', 'description', 'reply_text',
        'extracted_hashtag', 'tag'
    ]
    readonly_fields = ['datetime_robot']
    list_per_page = 20
    date_hierarchy = 'datetime_create'

    fieldsets = (
        ('اطلاعات پایه پست', {
            'fields': (
                'url', 'username', 'platform', 'province',
                'channel', 'media_type', 'lang_post'
            )
        }),
        ('محتوای پست', {
            'fields': (
                'description', 'reply_text', 'reply_username',
                'extracted_hashtag', 'extracted_mention', 'tag'
            )
        }),
        ('آمار و ارقام', {
            'fields': (
                'like_count', 'comment_count', 'view_count',
                'copy_count'
            )
        }),
        ('تحلیل و طبقه‌بندی', {
            'fields': (
                'sentiment', 'npo', 'emo', 'news_type',
                'news_topic'
            )
        }),
        ('متادیتا', {
            'fields': (
                'datetime_create', 'datetime_robot'
            )
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # اگر کاربر سوپر یوزر نیست، فقط پست‌های استان‌های مجاز را نشان بده
        if not request.user.is_superuser:
            user_provinces = UserProvinceAccess.objects.filter(
                user=request.user
            ).values_list('province_id', flat=True)
            qs = qs.filter(province_id__in=user_provinces)
        return qs


class UserProvinceAccessAdmin(admin.ModelAdmin):
    list_display = ['user', 'province', 'get_province_name_fa']
    list_filter = ['user', 'province']
    search_fields = ['user__username', 'province__name_fa']
    list_per_page = 20

    def get_province_name_fa(self, obj):
        return obj.province.name_fa

    get_province_name_fa.short_description = 'نام استان'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # اگر کاربر سوپر یوزر نیست، فقط دسترسی‌های خودش را ببیند
        if not request.user.is_superuser:
            qs = qs.filter(user=request.user)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # محدود کردن انتخاب کاربر در فرم
        if db_field.name == "user" and not request.user.is_superuser:
            kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# رجیستر مدل‌ها
admin.site.register(PoliticalCategory, PoliticalCategoryAdmin)
admin.site.register(UserCategory, UserCategoryAdmin)
admin.site.register(Channel, ChannelAdmin)
admin.site.register(Platform, PlatformAdmin)
admin.site.register(Province, ProvinceAdmin)
admin.site.register(NewsType, NewsTypeAdmin)
admin.site.register(NewsTopic, NewsTopicAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(UserProvinceAccess, UserProvinceAccessAdmin)