from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models import Count, Sum, Q
from django.utils.translation import gettext_lazy as _


class PoliticalCategory(models.Model):
    """دسته‌بندی سیاسی"""
    name = models.CharField(max_length=100, verbose_name=_("نام دسته‌بندی سیاسی"))
    description = models.TextField(blank=True, null=True, verbose_name=_("توضیحات"))

    class Meta:
        verbose_name = _("دسته‌بندی سیاسی")
        verbose_name_plural = _("دسته‌بندی‌های سیاسی")

    def __str__(self):
        return self.name


class UserCategory(models.Model):
    """دسته کاربری اصلی"""
    name = models.CharField(max_length=100, verbose_name=_("نام دسته کاربری"))
    description = models.TextField(blank=True, null=True, verbose_name=_("توضیحات"))

    class Meta:
        verbose_name = _("دسته کاربری")
        verbose_name_plural = _("دسته‌های کاربری")

    def __str__(self):
        return self.name


class Province(models.Model):
    name_fa = models.CharField(max_length=100, verbose_name=_("نام فارسی"))
    name_en = models.CharField(max_length=100, verbose_name=_("نام انگلیسی"))
    code = models.CharField(max_length=100, verbose_name=_("کد"))
    province_query = models.TextField(blank=True, null=True, verbose_name=_("کوئری استان"))

    class Meta:
        verbose_name = _("استان")
        verbose_name_plural = _("استان‌ها")

    def __str__(self):
        return f"{self.name_fa} - {self.name_en}"


class Platform(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("نام"))
    description = models.TextField(blank=True, null=True, verbose_name=_("توضیحات"))

    class Meta:
        verbose_name = _("پلتفرم")
        verbose_name_plural = _("پلتفرم‌ها")

    def __str__(self):
        return self.name


# مدل برای نوع خبر
class NewsType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("نام نوع خبر"))
    news_type_query = models.TextField(blank=True, null=True, verbose_name=_("توضیحات"))

    class Meta:
        verbose_name = _("نوع خبر")
        verbose_name_plural = _("انواع خبر")

    def __str__(self):
        return self.name


# مدل برای موضوع خبر
class NewsTopic(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("نام موضوع خبر"))
    news_topic_query = models.TextField(blank=True, null=True, verbose_name=_("توضیحات"))

    class Meta:
        verbose_name = _("موضوع خبر")
        verbose_name_plural = _("موضوعات خبر")

    def __str__(self):
        return self.name


class TvProgram(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("نام برنامه"))
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name=_("استان"))
    tv_program_query = models.TextField(blank=True, null=True, verbose_name=_("توضیحات"))

    class Meta:
        verbose_name = _("نام برنامه")
        verbose_name_plural = _("نام برنامه ها")

    def __str__(self):
        return self.name


class Channel(models.Model):
    CHANNEL_TYPE_CHOICES = [
        ('political', 'جریان سیاسی'),
        ('user_group', 'گروه کاربری'),
        ('no_type', 'فاقد نوع'),
    ]

    # اطلاعات پایه
    name_fa = models.CharField(max_length=100, verbose_name=_("نام فارسی کانال"))
    username = models.CharField(max_length=100, verbose_name=_("نام کاربری"))
    user_id = models.BigIntegerField(verbose_name=_("آیدی کاربری"))

    # دسته‌بندی‌های ForeignKey
    channel_type = models.CharField(max_length=20, choices=CHANNEL_TYPE_CHOICES, verbose_name=_("نوع کانال"))
    political_category = models.ForeignKey(
        PoliticalCategory,
        on_delete=models.SET_NULL,
        verbose_name=_("دسته‌بندی سیاسی"),
        null=True,
        blank=True,
        related_name='channels'
    )
    user_category = models.ForeignKey(
        UserCategory,
        on_delete=models.SET_NULL,
        verbose_name=_("دسته کاربری اصلی"),
        null=True,
        blank=True,
        related_name='channels'
    )

    # سایر فیلدها
    sub_category = models.CharField(max_length=100, verbose_name=_("دسته‌بندی فرعی"), blank=True, null=True)
    tag = models.CharField(max_length=100, verbose_name=_("تگ"), blank=True, null=True)
    platform = models.ForeignKey('Platform', on_delete=models.CASCADE, verbose_name=_("پلتفرم"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاریخ بروزرسانی"))

    class Meta:
        verbose_name = _("کانال")
        verbose_name_plural = _("کانال‌ها")
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['user_id']),
            models.Index(fields=['channel_type']),
            models.Index(fields=['political_category']),
            models.Index(fields=['user_category']),
            models.Index(fields=['platform']),
            models.Index(fields=['tag']),
        ]

    def __str__(self):
        return f"{self.name_fa} - {self.username}"

    def get_main_category(self):
        """برگرداندن دسته‌بندی اصلی بر اساس نوع کانال"""
        if self.channel_type == 'political' and self.political_category:
            return self.political_category.name
        elif self.channel_type == 'user_group' and self.user_category:
            return self.user_category.name
        return "بدون دسته‌بندی"


class Post(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('text', 'Text'),
        ('document', 'Document'),
    ]


    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
        ('notok', 'NotOK'),
    ]

    url = models.URLField(max_length=500, verbose_name=_("لینک پست"))
    lang_post = models.CharField(max_length=10, verbose_name=_("زبان پست"))
    like_count = models.IntegerField(default=0, verbose_name=_("تعداد لایک"))
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, verbose_name=_("نوع مدیا"))
    description = models.TextField(blank=True, null=True, verbose_name=_("توضیحات"))
    comment_count = models.IntegerField(default=0, verbose_name=_("تعداد کامنت"))
    username = models.CharField(max_length=100, verbose_name=_("نام کاربری"))
    extracted_hashtag = models.TextField(blank=True, null=True, verbose_name=_("هشتگ‌های استخراج شده"))
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, verbose_name=_("احساس"))
    npo = models.BooleanField(default=False, verbose_name=_("NPO"))
    emo = models.BooleanField(default=False, verbose_name=_("EMO"))
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE, verbose_name=_("پلتفرم"))
    tag = models.TextField(blank=True, null=True, verbose_name=_("تگ"))
    extracted_mention = models.TextField(blank=True, null=True, verbose_name=_("منشن‌های استخراج شده"))
    reply_text = models.TextField(blank=True, null=True, verbose_name=_("متن پاسخ"))
    reply_username = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("نام کاربری پاسخ دهنده"))
    datetime_create = models.DateTimeField(verbose_name=_("تاریخ ایجاد"))
    datetime_robot = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ربات"))
    # id_source = models.CharField(max_length=100, verbose_name=_("آیدی منبع"))
    view_count = models.IntegerField(default=0, verbose_name=_("تعداد بازدید"))
    copy_count = models.IntegerField(default=0, verbose_name=_("تعداد کپی"))
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name=_("استان"))
    # political_current = models.ForeignKey(
    #     PoliticalCurrent,
    #     on_delete=models.SET_NULL,
    #     verbose_name=_("جریان سیاسی"),
    #     null=True,
    #     blank=True
    # )
    #
    # user_group = models.ForeignKey(
    #     UserGroup,
    #     on_delete=models.SET_NULL,
    #     verbose_name=_("گروه کاربری"),
    #     null=True,
    #     blank=True
    # )

    channel = models.ForeignKey(
        Channel,
        on_delete=models.SET_NULL,
        verbose_name=_("کانال"),
        null=True,
        blank=True
    )


    news_type = models.ForeignKey(
        'NewsType',  # نام اپ و مدل
        on_delete=models.SET_NULL,
        verbose_name=_("نوع خبر"),
        null=True,
        blank=True
    )

    news_topic = models.ForeignKey(
        'NewsTopic',  # نام اپ و مدل
        on_delete=models.SET_NULL,
        verbose_name=_("موضوع خبر"),
        null=True,
        blank=True
    )

    tv_program = models.ForeignKey(
        'TvProgram',  # نام اپ و مدل
        on_delete=models.SET_NULL,
        verbose_name=_("نام برنامه"),
        null=True,
        blank=True
    )


    class Meta:
        verbose_name = _("پست")
        verbose_name_plural = _("پست‌ها")
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['datetime_create']),
            models.Index(fields=['province']),
            models.Index(fields=['platform']),
            models.Index(fields=['channel']),  # جایگزین شاخص‌های قبلی
            models.Index(fields=['news_type']),
            models.Index(fields=['news_topic']),
        ]

    def __str__(self):
        return f"{self.username} - {self.datetime_create}"


class UserProvinceAccess(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("کاربر"))
    province = models.ForeignKey(Province, on_delete=models.CASCADE, verbose_name=_("استان"))

    class Meta:
        verbose_name = _("دسترسی کاربر به استان")
        verbose_name_plural = _("دسترسی کاربران به استان‌ها")
        unique_together = ('user', 'province')

    def __str__(self):
        return f"{self.user.username} - {self.province.name_fa}"


class Profile(models.Model):
    # فیلدهای اصلی پروفایل
    name = models.CharField(max_length=255, verbose_name=_("نام اصلی"))
    position = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("سمت"))
    category = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("دسته"))
    photo = models.ImageField(upload_to='api/profiles/', blank=True, null=True, verbose_name=_("عکس"))
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name=_("استان"))

    # فیلدهای زمانی
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ایجاد"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("تاریخ بروزرسانی"))

    class Meta:
        verbose_name = _("پروفایل")
        verbose_name_plural = _("پروفایل‌ها")
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['category']),
            models.Index(fields=['position']),
            models.Index(fields=['province']),
        ]

    def __str__(self):
        return f"{self.name} - {self.position} - {self.province}"


class Celebrity(models.Model):
    # فیلد کلید خارجی به پروفایل
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name=_("پروفایل"),
        related_name='celebrities'
    )

    # فیلدهای کلید خارجی
    platform = models.ForeignKey('Platform', on_delete=models.CASCADE, verbose_name=_("پلتفرم"))

    # فیلدهای شناسه و آمار
    original_id = models.CharField(max_length=100, unique=True, verbose_name=_("آیدی"))
    member_count = models.IntegerField(default=0, verbose_name=_("تعداد اعضا"))

    # فیلدهای زمانی
    update_date = models.DateTimeField(auto_now=True, verbose_name=_("تاریخ آپدیت"))
    join_date = models.DateTimeField(verbose_name=_("تاریخ پیوستن"))

    class Meta:
        verbose_name = _("چهره")
        verbose_name_plural = _("چهره‌ها")
        indexes = [
            models.Index(fields=['platform']),
            models.Index(fields=['original_id']),
            models.Index(fields=['profile']),
        ]

    def __str__(self):
        return f"{self.profile.name} - {self.profile.position} - {self.platform}"

class CelebrityPost(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
        ('text', 'Text'),
        ('document', 'Document'),
    ]

    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
        ('notok', 'NotOK'),
    ]

    # ارتباط با مدل چهره
    celebrity = models.ForeignKey(
        Celebrity,
        on_delete=models.CASCADE,
        verbose_name=_("نام چهره"),
        related_name='posts'
    )

    # فیلدهای اصلی پست
    url = models.URLField(max_length=500, verbose_name=_("لینک پست"))
    lang_post = models.CharField(max_length=10, verbose_name=_("زبان پست"))
    like_count = models.IntegerField(default=0, verbose_name=_("تعداد لایک"))
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, verbose_name=_("نوع مدیا"))
    description = models.TextField(blank=True, null=True, verbose_name=_("توضیحات"))
    comment_count = models.IntegerField(default=0, verbose_name=_("تعداد کامنت"))
    # username = models.CharField(max_length=100, verbose_name=_("نام کاربری"))
    extracted_hashtag = models.TextField(blank=True, null=True, verbose_name=_("هشتگ‌های استخراج شده"))
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES, verbose_name=_("احساس"))
    npo = models.BooleanField(default=False, verbose_name=_("NPO"))
    emo = models.BooleanField(default=False, verbose_name=_("EMO"))

    # فیلدهای کلید خارجی
    platform = models.ForeignKey('Platform', on_delete=models.CASCADE, verbose_name=_("پلتفرم"))
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name=_("استان"))

    # فیلدهای متنی اضافی
    tag = models.TextField(blank=True, null=True, verbose_name=_("تگ"))
    extracted_mention = models.TextField(blank=True, null=True, verbose_name=_("منشن‌های استخراج شده"))
    reply_text = models.TextField(blank=True, null=True, verbose_name=_("متن پاسخ"))
    reply_username = models.CharField(max_length=100, blank=True, null=True, verbose_name=_("نام کاربری پاسخ دهنده"))

    # فیلدهای زمانی
    datetime_create = models.DateTimeField(verbose_name=_("تاریخ ایجاد"))
    datetime_robot = models.DateTimeField(auto_now_add=True, verbose_name=_("تاریخ ربات"))

    # فیلدهای آماری
    view_count = models.IntegerField(default=0, verbose_name=_("تعداد بازدید"))
    copy_count = models.IntegerField(default=0, verbose_name=_("تعداد کپی"))

    # فیلدهای کلید خارجی اختیاری
    # channel = models.ForeignKey(
    #     'Channel',
    #     on_delete=models.SET_NULL,
    #     verbose_name=_("کانال"),
    #     null=True,
    #     blank=True
    # )

    news_type = models.ForeignKey(
        'NewsType',
        on_delete=models.SET_NULL,
        verbose_name=_("نوع خبر"),
        null=True,
        blank=True
    )

    news_topic = models.ForeignKey(
        'NewsTopic',
        on_delete=models.SET_NULL,
        verbose_name=_("موضوع خبر"),
        null=True,
        blank=True
    )

    # tv_program = models.ForeignKey(
    #     'TvProgram',
    #     on_delete=models.SET_NULL,
    #     verbose_name=_("نام برنامه"),
    #     null=True,
    #     blank=True
    # )

    class Meta:
        verbose_name = _("پست چهره")
        verbose_name_plural = _("پست‌های چهره")
        indexes = [
            # models.Index(fields=['username']),
            models.Index(fields=['datetime_create']),
            models.Index(fields=['province']),
            models.Index(fields=['platform']),
            # models.Index(fields=['channel']),
            models.Index(fields=['news_type']),
            models.Index(fields=['news_topic']),
            models.Index(fields=['celebrity']),
            models.Index(fields=['sentiment']),
        ]

    def __str__(self):
        return f"{self.datetime_create} - {self.celebrity.profile.name}"


