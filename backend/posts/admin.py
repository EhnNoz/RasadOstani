# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Channel, Platform, Province, NewsType, NewsTopic,
    Post, UserProvinceAccess, PoliticalCategory, UserCategory, TvProgram, Celebrity, CelebrityPost, Profile
)
from django.utils.translation import gettext_lazy as _


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


class TvProgramAdmin(admin.ModelAdmin):
    list_display = ['name', 'province', 'tv_program_query']
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
                'news_topic','tv_program'
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


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'category', 'province', 'created_at', 'updated_at')
    list_filter = ('province', 'category', 'position')
    search_fields = ('name', 'position', 'category')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20

    fieldsets = (
        (_('اطلاعات اصلی'), {
            'fields': ('name', 'position', 'category', 'photo')
        }),
        (_('اطلاعات مکانی'), {
            'fields': ('province',)
        }),
        (_('تاریخ‌ها'), {
            'fields': ('created_at', 'updated_at')
        }),
    )


class CelebrityAdmin(admin.ModelAdmin):
    list_display = (
    'get_name', 'get_position', 'get_category', 'get_province', 'platform', 'member_count', 'update_date')
    list_filter = ('platform', 'profile__province', 'profile__category')
    search_fields = ('profile__name', 'original_id', 'profile__position')
    readonly_fields = ('update_date',)
    list_per_page = 20

    fieldsets = (
        (_('اطلاعات پروفایل'), {
            'fields': ('profile',)
        }),
        (_('اطلاعات پلتفرم'), {
            'fields': ('platform', 'original_id', 'member_count')
        }),
        (_('تاریخ‌ها'), {
            'fields': ('join_date', 'update_date')
        }),
    )

    # متدهای برای نمایش فیلدهای مرتبط از پروفایل
    def get_name(self, obj):
        return obj.profile.name

    get_name.short_description = _('نام')

    def get_position(self, obj):
        return obj.profile.position

    get_position.short_description = _('سمت')

    def get_category(self, obj):
        return obj.profile.category

    get_category.short_description = _('دسته')

    def get_province(self, obj):
        return obj.profile.province

    get_province.short_description = _('استان')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('profile', 'platform', 'profile__province')
        return queryset


class CelebrityPostAdmin(admin.ModelAdmin):
    list_display = (
    'celebrity', 'platform', 'media_type', 'sentiment', 'like_count', 'comment_count', 'datetime_create')
    list_filter = ('platform', 'province', 'media_type', 'sentiment', 'news_type', 'news_topic', 'datetime_create')
    search_fields = ('celebrity__name', 'description', 'extracted_hashtag', 'tag')
    readonly_fields = ('datetime_robot',)
    list_per_page = 25
    date_hierarchy = 'datetime_create'

    fieldsets = (
        (_('اطلاعات چهره و پلتفرم'), {
            'fields': ('celebrity', 'platform', 'province')
        }),
        (_('محتوای پست'), {
            'fields': ('url', 'lang_post', 'media_type', 'description', 'sentiment')
        }),
        (_('آمار و ارقام'), {
            'fields': ('like_count', 'comment_count', 'view_count', 'copy_count')
        }),
        (_('متادیتا و تگ‌ها'), {
            'fields': ('extracted_hashtag', 'tag', 'extracted_mention')
        }),
        (_('ویژگی‌های ویژه'), {
            'fields': ('npo', 'emo')
        }),
        (_('اطلاعات پاسخ'), {
            'fields': ('reply_text', 'reply_username')
        }),
        (_('دسته‌بندی محتوا'), {
            'fields': ('news_type', 'news_topic')
        }),
        (_('تاریخ‌ها'), {
            'fields': ('datetime_create', 'datetime_robot')
        }),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.select_related('celebrity', 'platform', 'province', 'news_type', 'news_topic')
        return queryset

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
admin.site.register(TvProgram, TvProgramAdmin)
# admin.site.register(Celebrity, CelebrityAdmin)
admin.site.register(CelebrityPost, CelebrityPostAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Celebrity, CelebrityAdmin)