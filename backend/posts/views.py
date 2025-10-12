from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta, datetime, date
from .models import Post, Platform, Province, UserProvinceAccess, Channel, UserCategory, PoliticalCategory
from .serializers import PostSerializer, PlatformSerializer, ProvinceSerializer, UserProvinceAccessSerializer, \
    ChannelSerializer, UserCategorySerializer, PoliticalCategorySerializer
from .filters import PostFilter, ProvinceStatsFilter, ChannelFilter, ProvinceFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
import jdatetime
from django.db.models import Count, Sum, Avg, F, ExpressionWrapper, FloatField
from django.db.models.functions import Coalesce
from collections import Counter
import re


class PlatformViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = Platform.objects.all()
        serializer = PlatformSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            platform = Platform.objects.get(pk=pk)
            serializer = PlatformSerializer(platform)
            return Response(serializer.data)
        except Platform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = PlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            platform = Platform.objects.get(pk=pk)
            serializer = PlatformSerializer(platform, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Platform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            platform = Platform.objects.get(pk=pk)
            serializer = PlatformSerializer(platform, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Platform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            platform = Platform.objects.get(pk=pk)
            platform.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Platform.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class ProvinceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProvinceFilter
    search_fields = ['name_fa', 'name_en']

    def get_queryset(self):
        queryset = Province.objects.all()

        # اعمال فیلترها
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)

        return queryset

    def list(self, request):
        queryset = self.get_queryset()
        serializer = ProvinceSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            province = Province.objects.get(pk=pk)
            serializer = ProvinceSerializer(province)
            return Response(serializer.data)
        except Province.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = ProvinceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            province = Province.objects.get(pk=pk)
            serializer = ProvinceSerializer(province, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Province.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            province = Province.objects.get(pk=pk)
            serializer = ProvinceSerializer(province, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Province.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            province = Province.objects.get(pk=pk)
            province.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Province.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class UserProvinceAccessViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = UserProvinceAccess.objects.all()
        serializer = UserProvinceAccessSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            access = UserProvinceAccess.objects.get(pk=pk)
            serializer = UserProvinceAccessSerializer(access)
            return Response(serializer.data)
        except UserProvinceAccess.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = UserProvinceAccessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            access = UserProvinceAccess.objects.get(pk=pk)
            serializer = UserProvinceAccessSerializer(access, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProvinceAccess.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            access = UserProvinceAccess.objects.get(pk=pk)
            serializer = UserProvinceAccessSerializer(access, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProvinceAccess.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            access = UserProvinceAccess.objects.get(pk=pk)
            access.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserProvinceAccess.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PoliticalCategoryViewSet(viewsets.ModelViewSet):
    queryset = PoliticalCategory.objects.all()
    serializer_class = PoliticalCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']

class UserCategoryViewSet(viewsets.ModelViewSet):
    queryset = UserCategory.objects.all()
    serializer_class = UserCategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ChannelFilter  # استفاده از فیلتر اختصاصی
    search_fields = ['name_fa', 'username', 'political_category__name', 'user_category__name', 'tag', 'sub_category']


class PostViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _get_filtered_queryset(self, request):
        """متد کمکی برای فیلتر کردن queryset"""
        user = request.user

        # فیلتر بر اساس دسترسی کاربر
        if user.is_superuser:
            queryset = Post.objects.all()
        else:
            user_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province_id', flat=True)
            queryset = Post.objects.filter(province_id__in=user_provinces)

        # اعمال فیلترهای اضافی
        post_filter = PostFilter(request.query_params, queryset=queryset)
        return post_filter.qs

    def list(self, request):
        queryset = self._get_filtered_queryset(request)

        # جستجو
        search_term = request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(
                Q(username__icontains=search_term) |
                Q(description__icontains=search_term) |
                Q(reply_text__icontains=search_term)
            )

        # دریافت نوع مرتب‌سازی از پارامترهای درخواست
        sort_by = request.query_params.get('sort_by', 'newest')

        # اعمال مرتب‌سازی بر اساس نوع درخواست شده
        if sort_by == 'likes':
            queryset = queryset.order_by('-like_count')[:20]
        elif sort_by == 'views':
            queryset = queryset.order_by('-view_count')[:20]
        elif sort_by == 'newest':
            queryset = queryset.order_by('-datetime_create')[:20]
        else:
            # حالت پیش‌فرض - 20 پست جدیدترین
            queryset = queryset.order_by('-datetime_create')[:20]

        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    # سایر متدها بدون تغییر باقی می‌مانند...
    def retrieve(self, request, pk=None):
        try:
            # بررسی دسترسی کاربر به پست
            post = Post.objects.get(pk=pk)
            user = request.user

            if not user.is_superuser:
                user_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province_id', flat=True)
                if post.province_id not in user_provinces:
                    return Response(
                        {"detail": "You do not have permission to access this post."},
                        status=status.HTTP_403_FORBIDDEN
                    )

            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            user = request.user

            # بررسی دسترسی
            if not user.is_superuser:
                user_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province_id', flat=True)
                if post.province_id not in user_provinces:
                    return Response(
                        {"detail": "You do not have permission to update this post."},
                        status=status.HTTP_403_FORBIDDEN
                    )

            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            user = request.user

            # بررسی دسترسی
            if not user.is_superuser:
                user_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province_id', flat=True)
                if post.province_id not in user_provinces:
                    return Response(
                        {"detail": "You do not have permission to update this post."},
                        status=status.HTTP_403_FORBIDDEN
                    )

            serializer = PostSerializer(post, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            user = request.user

            # بررسی دسترسی
            if not user.is_superuser:
                user_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province_id', flat=True)
                if post.province_id not in user_provinces:
                    return Response(
                        {"detail": "You do not have permission to delete this post."},
                        status=status.HTTP_403_FORBIDDEN
                    )

            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        queryset = self._get_filtered_queryset(request)

        # آمار کلی
        total_posts = queryset.count()
        unique_users = queryset.values('username').distinct().count()
        total_views = queryset.aggregate(total_views=Sum('view_count'))['total_views'] or 0
        total_likes = queryset.aggregate(total_likes=Sum('like_count'))['total_likes'] or 0

        # روند روزانه — استفاده از DATE(datetime_create) برای گروه‌بندی بر اساس تاریخ
        daily_trend_qs = queryset.extra(
            select={'date': "DATE(datetime_create)"}
        ).values('date').annotate(
            posts=Count('id'),
            views=Sum('view_count'),
            likes=Sum('like_count')
        ).order_by('date')

        # تبدیل تاریخ‌ها به شمسی و آماده‌سازی داده‌ها
        categories = []
        post_data = []
        view_data = []
        like_data = []

        for item in daily_trend_qs:
            gregorian_date = item['date']  # datetime.date
            print(gregorian_date)
            # تبدیل به datetime.date اگر datetime.datetime بود
            if isinstance(gregorian_date, datetime):
                gregorian_date = gregorian_date.date()
            elif isinstance(gregorian_date, str):
                # اگر رشته بود، سعی در پارس کنیم
                try:
                    from dateutil import parser
                    gregorian_date = parser.parse(gregorian_date).date()
                except:
                    continue  # یا خطای مناسب
            elif not isinstance(gregorian_date, date):
                continue  # داده نامعتبر — ازش بگذر

            # حالا تبدیل به شمسی
            try:
                jalali_date = jdatetime.date.fromgregorian(date=gregorian_date)
                jalali_str = f"{jalali_date.year:04d}-{jalali_date.month:02d}-{jalali_date.day:02d}"
            except (ValueError, OverflowError) as e:
                continue  # تاریخ خارج از محدوده معتبر (مثلاً قبل از 1600 میلادی)


            categories.append(jalali_str)
            post_data.append(item['posts'])
            view_data.append(item['views'])
            like_data.append(item['likes'])

        # ساخت ساختار نهایی برای نمودار
        daily_trend = [
            {
                "name": "تعداد پست‌ها",
                "categories": categories,
                "data": post_data,
                "color": "#b2532f"
            },
            {
                "name": "تعداد بازدیدها",
                "categories": categories,
                "data": view_data,
                "color": "#4CAF50"
            },
            {
                "name": "تعداد لایک‌ها",
                "categories": categories,
                "data": like_data,
                "color": "#2196F3"
            }
        ]

        data = {
            'total_posts': total_posts,
            'unique_users': unique_users,
            'total_views': total_views,
            'total_likes': total_likes,
            'daily_trend': daily_trend
        }

        return Response(data)


class ProvinceStatsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _get_filtered_queryset(self, request):
        """متد کمکی برای فیلتر کردن queryset بر اساس دسترسی کاربر"""
        user = request.user

        # فیلتر بر اساس دسترسی کاربر
        if user.is_superuser:
            queryset = Post.objects.all()
        else:
            user_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province_id', flat=True)
            queryset = Post.objects.filter(province_id__in=user_provinces)

        # اعمال فیلترهای اضافی
        stats_filter = ProvinceStatsFilter(request.query_params, queryset=queryset)
        return stats_filter.qs

    def list(self, request):
        """Endpoint برای آمار پست‌ها به تفکیک استان"""
        queryset = self._get_filtered_queryset(request)

        # فیلتر بر اساس تاریخ (پیش‌فرض ۷ روز اخیر)
        start_date_param = request.query_params.get('start_date')
        end_date_param = request.query_params.get('end_date')

        if not start_date_param and not end_date_param:
            default_end_date = timezone.now()
            default_start_date = default_end_date - timedelta(days=120)
            queryset = queryset.filter(
                datetime_create__range=(default_start_date, default_end_date)
            )

        # گروه‌بندی بر اساس استان و شمارش پست‌ها
        province_stats = queryset.values(
            'province__name_en',
            'province__name_fa',
            'province__code'  # اضافه کردن فیلد کد استان
        ).annotate(
            post_count=Count('id')
        ).order_by('-post_count')

        # تبدیل به فرمت مورد نظر
        data = [
            [f"ir-{stat['province__code']}", stat['post_count']]
            for stat in province_stats
        ]

        return Response(data)

# class PoliticalCurrentViewSet(viewsets.ModelViewSet):
#     queryset = PoliticalCurrent.objects.all()
#     serializer_class = PoliticalCurrentSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     search_fields = ['username', 'main_current', 'sub_current', 'tag']
#
#
# class UserGroupViewSet(viewsets.ModelViewSet):
#     queryset = UserGroup.objects.all()
#     serializer_class = UserGroupSerializer
#     permission_classes = [IsAuthenticated]
#     filter_backends = [DjangoFilterBackend, SearchFilter]
#     search_fields = ['username', 'main_group', 'sub_group', 'tag']


def prepare_chart_data(queryset, value_field, name_field='username', colors=None):
    if colors is None:
        colors = [
            "#fe7743", "#b2532f", "#9b4929", "#d98a5e", "#f0a582",
            "#c16a43", "#a55a3a", "#e57e4d", "#ff8e5c", "#b85e38"
        ]

    categories = []
    data = []

    for idx, item in enumerate(queryset):
        username = item[name_field]
        value = item[value_field]

        categories.append(username)
        color = colors[idx % len(colors)]
        data.append({"y": value, "color": color})

    return {
        "categories": categories,
        "data": data
    }


def prepare_pie_series(data_list, name_field, count_field, colors=None):
    """
    تبدیل لیست داده به فرمت سری نمودار (مثل pie یا bar)
    """
    if colors is None:
        colors = [
            "#fe7743", "#b2532f", "#9b4929", "#d98a5e", "#f0a582",
            "#c16a43", "#a55a3a", "#e57e4d", "#ff8e5c", "#b85e38"
        ]

    result = []
    for idx, item in enumerate(data_list):
        name = item[name_field]
        count = item[count_field]
        color = colors[idx % len(colors)]
        result.append({
            "name": name,
            "y": count,
            "color": color
        })
    return result


# views.py - در AdvancedAnalyticsViewSet
class AdvancedAnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _get_filtered_queryset(self, request):
        """متد کمکی برای فیلتر کردن queryset بر اساس دسترسی کاربر"""
        user = request.user

        if user.is_superuser:
            queryset = Post.objects.all()
        else:
            user_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province_id', flat=True)
            queryset = Post.objects.filter(province_id__in=user_provinces)

        post_filter = PostFilter(request.query_params, queryset=queryset)
        return post_filter.qs

    def list(self, request):
        queryset = self._get_filtered_queryset(request)

        # آمار کلی
        total_posts = queryset.count()
        total_likes = queryset.aggregate(total=Coalesce(Sum('like_count'), 0))['total'] or 0
        total_views = queryset.aggregate(total=Coalesce(Sum('view_count'), 0))['total'] or 0

        # محاسبه درصد نسبت به کل
        all_posts_queryset = Post.objects.all()
        all_posts_filter = PostFilter(request.query_params, queryset=all_posts_queryset)
        all_posts_filtered = all_posts_filter.qs

        all_posts_count = all_posts_filtered.count() or 1
        all_likes = all_posts_filtered.aggregate(total=Coalesce(Sum('like_count'), 0))['total'] or 1
        all_views = all_posts_filtered.aggregate(total=Coalesce(Sum('view_count'), 0))['total'] or 1

        post_percentage = (total_posts / all_posts_count * 100) if all_posts_count > 0 else 0
        like_percentage = (total_likes / all_likes * 100) if all_likes > 0 else 0
        view_percentage = (total_views / all_views * 100) if all_views > 0 else 0

        # ابر هشتگها
        all_hashtags = []
        for post in queryset.exclude(extracted_hashtag__isnull=True).exclude(extracted_hashtag=''):
            if post.extracted_hashtag:
                hashtags = post.extracted_hashtag.split(' ')
                all_hashtags.extend([tag.strip() for tag in hashtags if tag.strip()])

        hashtag_counter = Counter(all_hashtags)
        top_hashtags = [{'name': tag, 'weight': count} for tag, count in hashtag_counter.most_common(30)]

        # کاربران موثر و فعال
        top_users_by_likes_qs = (queryset.values('username')
                                     .annotate(total_likes=Sum('like_count'))
                                     .order_by('-total_likes')[:20])
        top_users_by_likes = prepare_chart_data(top_users_by_likes_qs, 'total_likes')

        top_users_by_views_qs = (queryset.values('username')
                                     .annotate(total_views=Sum('view_count'))
                                     .order_by('-total_views')[:20])
        top_users_by_views = prepare_chart_data(top_users_by_views_qs, 'total_views')

        active_users_qs = (queryset.values('username')
                               .annotate(post_count=Count('id'))
                               .order_by('-post_count')[:20])
        active_users = prepare_chart_data(active_users_qs, 'post_count')

        # فعالترین کانال‌ها
        active_channels_qs = (queryset.exclude(channel__isnull=True)
                                  .values('channel__name_fa', 'channel__channel_type')
                                  .annotate(post_count=Count('id'))
                                  .order_by('-post_count')[:10])

        active_channels = prepare_pie_series(
            list(active_channels_qs),
            name_field='channel__name_fa',
            count_field='post_count'
        )

        # توزیع کانال‌ها بر اساس نوع
        channel_type_stats = (queryset.exclude(channel__isnull=True)
                              .values('channel__channel_type')
                              .annotate(count=Count('id'))
                              .order_by('-count'))

        channel_type_distribution = prepare_pie_series(
            list(channel_type_stats),
            name_field='channel__channel_type',
            count_field='count'
        )

        # فراوانی جریانات سیاسی (بر اساس تعداد پست)
        political_currents_stats = (queryset.exclude(channel__political_category__isnull=True)
                                    .values('channel__political_category__name')
                                    .annotate(
                                        post_count=Count('id'),
                                        total_likes=Sum('like_count'),
                                        total_views=Sum('view_count')
                                    )
                                    .order_by('-post_count')[:15])

        political_currents_distribution = prepare_pie_series(
            list(political_currents_stats),
            name_field='channel__political_category__name',
            count_field='post_count'
        )

        # فراوانی گروه‌های کاربری (بر اساس تعداد پست)
        user_groups_stats = (queryset.exclude(channel__user_category__isnull=True)
                             .values('channel__user_category__name')
                             .annotate(
                                 post_count=Count('id'),
                                 total_likes=Sum('like_count'),
                                 total_views=Sum('view_count')
                             )
                             .order_by('-post_count')[:15])

        user_groups_distribution = prepare_pie_series(
            list(user_groups_stats),
            name_field='channel__user_category__name',
            count_field='post_count'
        )

        # فراوانی احساسات
        sentiment_stats = (queryset.values('sentiment')
                           .annotate(count=Count('id'))
                           .order_by('-count'))

        # محاسبه درصد احساسات
        sentiment_data = []
        for stat in sentiment_stats:
            percentage = (stat['count'] / total_posts * 100) if total_posts > 0 else 0
            sentiment_data.append({
                'sentiment': stat['sentiment'],
                'count': stat['count'],
                'percentage': round(percentage, 2)
            })

        # آمار NPO و EMO
        npo_count = queryset.filter(npo=True).count()
        emo_count = queryset.filter(emo=True).count()

        npo_stats = {
            'total_npo': npo_count,
            'npo_percentage': round((npo_count / total_posts * 100) if total_posts > 0 else 0, 2)
        }

        emo_stats = {
            'total_emo': emo_count,
            'emo_percentage': round((emo_count / total_posts * 100) if total_posts > 0 else 0, 2)
        }

        # Heatmap موضوعات
        today = datetime.now().date()
        dates_gregorian = [today - timedelta(days=i) for i in range(6, -1, -1)]

        dates_categories = []
        for date in dates_gregorian:
            try:
                jalali_date = jdatetime.date.fromgregorian(date=date)
                dates_categories.append(jalali_date.strftime("%Y-%m-%d"))
            except:
                dates_categories.append(date.strftime("%Y-%m-%d"))

        heatmap_queryset = Post.objects.filter(
            datetime_create__date__gte=dates_gregorian[0],
            datetime_create__date__lte=dates_gregorian[-1]
        )

        user = request.user
        if not user.is_superuser:
            user_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province_id', flat=True)
            heatmap_queryset = heatmap_queryset.filter(province_id__in=user_provinces)

        top_topics_qs = (heatmap_queryset
                             .exclude(news_topic__isnull=True)
                             .values('news_topic__id', 'news_topic__name')
                             .annotate(count=Count('id'))
                             .order_by('-count')[:10])

        topics_categories = [topic['news_topic__name'] for topic in top_topics_qs]
        topic_ids = [topic['news_topic__id'] for topic in top_topics_qs]

        heatmap_data = []
        for date_idx, gregorian_date in enumerate(dates_gregorian):
            for topic_idx, topic_id in enumerate(topic_ids):
                count = heatmap_queryset.filter(
                    news_topic_id=topic_id,
                    datetime_create__date=gregorian_date
                ).count()
                heatmap_data.append([date_idx, topic_idx, count])

        topics_heatmap = {
            'xAxis': {
                'categories': dates_categories,
                'title': {'text': 'تاریخ (شمسی)'}
            },
            'yAxis': {
                'categories': topics_categories,
                'title': {'text': 'موضوعات'},
                'reversed': True
            },
            'series': [{
                'name': 'تعداد پست‌ها',
                'borderWidth': 1,
                'data': heatmap_data
            }]
        }

        data = {
            'overall_stats': {
                'total_posts': total_posts,
                'total_likes': total_likes,
                'total_views': total_views,
                'post_percentage': round(post_percentage, 2),
                'like_percentage': round(like_percentage, 2),
                'view_percentage': round(view_percentage, 2)
            },
            'top_hashtags': top_hashtags,
            'top_users_by_likes': top_users_by_likes,
            'top_users_by_views': top_users_by_views,
            'active_users': active_users,
            'active_channels': active_channels,
            'channel_type_distribution': channel_type_distribution,
            'political_currents_distribution': political_currents_distribution,
            'user_groups_distribution': user_groups_distribution,
            'sentiment_distribution': sentiment_data,
            'npo_stats': npo_stats,
            'emo_stats': emo_stats,
            'topics_heatmap': topics_heatmap
        }

        return Response(data)