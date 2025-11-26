import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q
import jdatetime
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Post, Channel, Province, UserCategory, NewsType, NewsTopic, PoliticalCategory, Platform, Profile, \
    TvProgram
from django_filters.rest_framework import BaseInFilter, NumberFilter, CharFilter
from django.contrib.postgres.search import SearchQuery
import logging


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class CharInFilter(BaseInFilter, CharFilter):
    pass


class PostFilter(django_filters.FilterSet):
    # فیلترهای چند انتخابی با فرمت CSV
    platform = NumberInFilter(field_name='platform__id', lookup_expr='in')
    platform_names = CharInFilter(field_name='platform__name', lookup_expr='in')
    province = django_filters.CharFilter(method='filter_province')
    channel = NumberInFilter(field_name='channel__id', lookup_expr='in')

    channel_type = django_filters.MultipleChoiceFilter(
        field_name='channel__channel_type',
        choices=Post.Channel.CHANNEL_TYPE_CHOICES if hasattr(Post, 'Channel') else []
        # یا مستقیماً از مدل Channel ایمپورت کنید:
        # choices=Channel.CHANNEL_TYPE_CHOICES
    )

    political_category = NumberInFilter(field_name='channel__political_category__id', lookup_expr='in')
    user_category = NumberInFilter(field_name='channel__user_category__id', lookup_expr='in')
    news_type = NumberInFilter(field_name='news_type__id', lookup_expr='in')
    news_topic = NumberInFilter(field_name='news_topic__id', lookup_expr='in')

    # فیلترهای چند انتخابی برای احساسات و مدیا
    sentiment = django_filters.MultipleChoiceFilter(
        field_name='sentiment',
        choices=Post.SENTIMENT_CHOICES
    )

    media_type = django_filters.MultipleChoiceFilter(
        field_name='media_type',
        choices=Post.MEDIA_TYPE_CHOICES
    )

    # فیلترهای بولین
    npo = django_filters.BooleanFilter(field_name='npo')
    emo = django_filters.BooleanFilter(field_name='emo')

    # فیلترهای تاریخ و جستجو
    start_date = django_filters.CharFilter(method='filter_start_date')
    end_date = django_filters.CharFilter(method='filter_end_date')
    search = django_filters.CharFilter(method='filter_search')

    # فیلترهای متنی برای جستجوی جزئی (اختیاری — دیگر در جستجوی اصلی استفاده نمی‌شوند)
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')
    channel_name = django_filters.CharFilter(field_name='channel__name_fa', lookup_expr='icontains')

    class Meta:
        model = Post
        fields = [
            'platform', 'platform_names', 'province', 'channel', 'channel_type',
            'political_category', 'user_category', 'news_type', 'news_topic',
            'sentiment', 'media_type', 'npo', 'emo', 'start_date', 'end_date', 'search'
        ]

    def filter_province(self, queryset, name, value):
        """فیلتر استان بر اساس ID یا name_en"""
        if value.isdigit():
            return queryset.filter(province__id=value)
        else:
            return queryset.filter(province__name_en__iexact=value)

    def filter_start_date(self, queryset, name, value):
        """فیلتر تاریخ شروع (شمسی به میلادی)"""
        try:
            jd = jdatetime.datetime.strptime(value, '%Y/%m/%d')
            gregorian_date = jd.togregorian()
            return queryset.filter(datetime_create__gte=gregorian_date)
        except (ValueError, TypeError):
            return queryset

    def filter_end_date(self, queryset, name, value):
        """فیلتر تاریخ پایان (شمسی به میلادی)"""
        try:
            jd = jdatetime.datetime.strptime(value, '%Y/%m/%d')
            gregorian_date = jd.togregorian()
            # پایان روز
            end_of_day = gregorian_date + timedelta(days=1)
            return queryset.filter(datetime_create__lte=end_of_day)
        except (ValueError, TypeError):
            return queryset

    print("*///////////*")
    logger = logging.getLogger(__name__)
    print("***************")

    def filter_search(self, queryset, name, value):
        if not value or not value.strip():
            return queryset

        try:
            # ✅ فعال‌سازی پشتیبانی از AND/OR/NOT با search_type='raw'
            query = SearchQuery(value, search_type='raw', config='simple')
            return queryset.filter(search_vector=query)
        except Exception as e:
            # در صورت خطا (مثلاً سینتکس نامعتبر)، جستجوی ساده با حالت 'plain' انجام شود
            # logger.warning(f"Raw search failed for '{value}': {e}")
            query = SearchQuery(value, search_type='plain', config='simple')
            return queryset.filter(search_vector=query)

    @property
    def qs(self):
        """
        اعمال فیلتر پیش‌فرض (7 روز اخیر) اگر هیچ تاریخی داده نشده باشد
        """
        queryset = super().qs

        has_start = 'start_date' in self.data
        has_end = 'end_date' in self.data

        if not has_start and not has_end:
            # فیلتر پیش‌فرض: 7 روز اخیر
            seven_days_ago = timezone.now().date() - timedelta(days=7)
            queryset = queryset.filter(datetime_create__date__gte=seven_days_ago)

        return queryset

class ProvinceStatsFilter(django_filters.FilterSet):
    # فیلترهای چند انتخابی با فرمت CSV
    platform = NumberInFilter(field_name='platform__id', lookup_expr='in')
    # province = NumberInFilter(field_name='province__id', lookup_expr='in')
    province = django_filters.CharFilter(method='filter_province')
    channel = NumberInFilter(field_name='channel__id', lookup_expr='in')

    channel_type = django_filters.MultipleChoiceFilter(
        field_name='channel__channel_type',
        choices=Channel.CHANNEL_TYPE_CHOICES
    )

    political_category = NumberInFilter(field_name='channel__political_category__id', lookup_expr='in')
    user_category = NumberInFilter(field_name='channel__user_category__id', lookup_expr='in')
    news_type = NumberInFilter(field_name='news_type__id', lookup_expr='in')
    news_topic = NumberInFilter(field_name='news_topic__id', lookup_expr='in')

    # فیلترهای دیگر
    sentiment = django_filters.MultipleChoiceFilter(
        field_name='sentiment',
        choices=Post.SENTIMENT_CHOICES
    )

    start_date = django_filters.CharFilter(method='filter_start_date')
    end_date = django_filters.CharFilter(method='filter_end_date')
    search = django_filters.CharFilter(method='filter_search')

    def filter_province(self, queryset, name, value):
        # اگر عدد باشد (ID)
        if value.isdigit():
            return queryset.filter(province__id=value)
        # اگر رشته باشد (name_en)
        else:
            return queryset.filter(province__name_en__iexact=value)

    class Meta:
        model = Post
        fields = [
            'platform', 'province', 'channel', 'channel_type',
            'political_category', 'user_category', 'sentiment', 'news_type',
            'news_topic', 'start_date', 'end_date', 'search'
        ]

    def filter_start_date(self, queryset, name, value):
        try:
            jd = jdatetime.strptime(value, '%Y/%m/%d')
            md = jd.togregorian()
            return queryset.filter(datetime_create__gte=md)
        except (ValueError, TypeError):
            return queryset

    def filter_end_date(self, queryset, name, value):
        try:
            jd = jdatetime.strptime(value, '%Y/%m/%d')
            md = jd.togregorian()
            md = md + timezone.timedelta(days=1)
            return queryset.filter(datetime_create__lte=md)
        except (ValueError, TypeError):
            return queryset

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(username__icontains=value) |
            Q(description__icontains=value) |
            Q(reply_text__icontains=value) |
            Q(channel__name_fa__icontains=value)
        )

    @property
    def qs(self):
        queryset = super().qs

        has_start = 'start_date' in self.data
        has_end = 'end_date' in self.data

        if not has_start and not has_end:
            seven_days_ago = timezone.now().date() - timedelta(days=7)
            queryset = queryset.filter(datetime_create__date__gte=seven_days_ago)

        return queryset


# filters.py - اضافه کردن ChannelFilter
class ChannelFilter(django_filters.FilterSet):
    # فیلترهای چند انتخابی
    channel_type = django_filters.MultipleChoiceFilter(
        field_name='channel_type',
        choices=Channel.CHANNEL_TYPE_CHOICES
    )

    platform = NumberInFilter(field_name='platform__id', lookup_expr='in')
    platform_names = CharInFilter(field_name='platform__name', lookup_expr='in')
    political_category = NumberInFilter(field_name='political_category__id', lookup_expr='in')
    user_category = NumberInFilter(field_name='user_category__id', lookup_expr='in')

    # فیلترهای متنی برای جستجوی جزئی
    name_fa = django_filters.CharFilter(field_name='name_fa', lookup_expr='icontains')
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')

    # فیلترهای عددی
    user_id = django_filters.NumberFilter(field_name='user_id')
    platform_id = django_filters.NumberFilter(field_name='platform__id')
    political_category_id = django_filters.NumberFilter(field_name='political_category__id')
    user_category_id = django_filters.NumberFilter(field_name='user_category__id')

    # فیلترهای متنی برای تگ و زیردسته
    tag = django_filters.CharFilter(field_name='tag', lookup_expr='icontains')
    sub_category = django_filters.CharFilter(field_name='sub_category', lookup_expr='icontains')

    # فیلترهای تاریخ
    created_after = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    updated_after = django_filters.DateFilter(field_name='updated_at', lookup_expr='gte')
    updated_before = django_filters.DateFilter(field_name='updated_at', lookup_expr='lte')

    # فیلتر ترکیبی برای جستجو
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Channel
        fields = [
            'channel_type', 'platform', 'platform_names', 'political_category',
            'user_category', 'name_fa', 'username', 'user_id', 'tag', 'sub_category'
        ]

    def filter_search(self, queryset, name, value):
        """فیلتر جستجوی ترکیبی در چند فیلد"""
        return queryset.filter(
            Q(name_fa__icontains=value) |
            Q(username__icontains=value) |
            Q(tag__icontains=value) |
            Q(sub_category__icontains=value) |
            Q(political_category__name__icontains=value) |
            Q(user_category__name__icontains=value) |
            Q(platform__name__icontains=value)
        )


class ProvinceFilter(django_filters.FilterSet):
    # فیلترهای متنی برای جستجوی جزئی
    name_fa = django_filters.CharFilter(field_name='name_fa', lookup_expr='icontains')
    name_en = django_filters.CharFilter(field_name='name_en', lookup_expr='icontains')

    # فیلتر ترکیبی برای جستجو
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = Province
        fields = ['name_fa', 'name_en']

    def filter_search(self, queryset, name, value):
        """فیلتر جستجوی ترکیبی در نام فارسی و انگلیسی"""
        return queryset.filter(
            Q(name_fa__icontains=value) |
            Q(name_en__icontains=value)
        )


class ProfileFilter(django_filters.FilterSet):
    province = django_filters.CharFilter(method='filter_province')
    name = django_filters.CharFilter(lookup_expr='icontains')
    position = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.CharFilter(lookup_expr='icontains')


    class Meta:
        model = Profile
        fields = ['name', 'position', 'category']

    def filter_province(self, queryset, name, value):
        if value.isdigit():
            return queryset.filter(province__id=value)
        else:
            return queryset.filter(province__name_en__iexact=value)


class TvProgramFilter(django_filters.FilterSet):
    # فیلترهای چند انتخابی
    province = NumberInFilter(field_name='province__id', lookup_expr='in')
    province_names = CharInFilter(field_name='province__name_fa', lookup_expr='in')

    # فیلتر متنی برای نام برنامه
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    # فیلتر جستجوی ترکیبی
    search = django_filters.CharFilter(method='filter_search')

    # فیلتر استان با نام انگلیسی
    province_en = django_filters.CharFilter(field_name='province__name_en', lookup_expr='iexact')

    class Meta:
        model = TvProgram
        fields = ['name', 'province', 'province_names', 'province_en', 'search']

    def filter_search(self, queryset, name, value):
        """فیلتر جستجوی ترکیبی در نام برنامه و توضیحات"""
        return queryset.filter(
            Q(name__icontains=value) |
            Q(tv_program_query__icontains=value) |
            Q(province__name_fa__icontains=value) |
            Q(province__name_en__icontains=value)
        )


