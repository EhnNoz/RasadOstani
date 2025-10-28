from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta, datetime, date
from .models import Post, Platform, Province, UserProvinceAccess, Channel, UserCategory, PoliticalCategory, NewsType, \
    NewsTopic
from .serializers import PostSerializer, PlatformSerializer, ProvinceSerializer, UserProvinceAccessSerializer, \
    ChannelSerializer, UserCategorySerializer, PoliticalCategorySerializer, NewsTypeSerializer, NewsTopicSerializer
from .filters import PostFilter, ProvinceStatsFilter, ChannelFilter, ProvinceFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
import jdatetime
from jdatetime import date as jdate
from django.db.models import Count, Sum, Avg, F, ExpressionWrapper, FloatField
from django.db.models.functions import Coalesce
from collections import Counter, defaultdict
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


class NewsTypeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = NewsType.objects.all()
        serializer = NewsTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            newstype = NewsType.objects.get(pk=pk)
            serializer = NewsTypeSerializer(newstype)
            return Response(serializer.data)
        except NewsType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = NewsTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            newstype = NewsType.objects.get(pk=pk)
            serializer = NewsTypeSerializer(newstype, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NewsType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            newstype = NewsType.objects.get(pk=pk)
            serializer = NewsTypeSerializer(newstype, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NewsType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            newstype = NewsType.objects.get(pk=pk)
            newstype.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NewsType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class NewsTopicViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = NewsTopic.objects.all()
        serializer = NewsTopicSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            newstopic = NewsTopic.objects.get(pk=pk)
            serializer = NewsTopicSerializer(newstopic)
            return Response(serializer.data)
        except NewsType.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = NewsTopicSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            newstopic = NewsTopic.objects.get(pk=pk)
            serializer = NewsTopicSerializer(newstopic, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NewsTopic.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            newstopic = NewsTopic.objects.get(pk=pk)
            serializer = NewsTopicSerializer(newstopic, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except NewsTopic.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            newstopic = NewsTopic.objects.get(pk=pk)
            newstopic.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except NewsTopic.DoesNotExist:
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

    def retrieve(self, request, pk=None):
        try:
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
        daily_categories = []
        daily_post_data = []
        daily_view_data = []
        daily_like_data = []

        for item in daily_trend_qs:
            gregorian_date = item['date']

            if isinstance(gregorian_date, datetime):
                gregorian_date = gregorian_date.date()
            elif isinstance(gregorian_date, str):
                try:
                    from dateutil import parser
                    gregorian_date = parser.parse(gregorian_date).date()
                except:
                    continue
            elif not isinstance(gregorian_date, date):
                continue

            try:
                jalali_date = jdate.fromgregorian(date=gregorian_date)
                jalali_str = f"{jalali_date.year:04d}-{jalali_date.month:02d}-{jalali_date.day:02d}"
            except (ValueError, OverflowError):
                continue

            daily_categories.append(jalali_str)
            daily_post_data.append(item['posts'])
            daily_view_data.append(item['views'])
            daily_like_data.append(item['likes'])

        # ساخت ساختار نهایی برای نمودارها
        daily_trend = {
            "name": "روند روزانه پست‌ها",
            "categories": daily_categories,
            "data": daily_post_data,
            "color": "#A281DD"
        }

        view_trend = {
            "name": "روند بازدیدها",
            "categories": daily_categories,
            "data": daily_view_data,
            "color": "#A281DD"
        }

        like_trend = {
            "name": "روند لایک‌ها",
            "categories": daily_categories,
            "data": daily_like_data,
            "color": "#A281DD"
        }

        # --- استخراج 5 هشتگ برتر و استان‌های مرتبط ---
        posts_with_hashtags = queryset.filter(
            extracted_hashtag__isnull=False
        ).exclude(
            extracted_hashtag=''
        ).select_related('province').values('extracted_hashtag', 'province__name_fa')

        hashtag_provinces = defaultdict(set)
        hashtag_counter = Counter()

        for post in posts_with_hashtags:
            hashtags_text = post['extracted_hashtag']
            province_name = post['province__name_fa']
            raw_tags = hashtags_text.split()
            for tag in raw_tags:
                clean_tag = re.sub(r'[^\w#آ-ی]', '', tag)
                if clean_tag.startswith('#') and len(clean_tag) > 1:
                    hashtag_provinces[clean_tag].add(province_name)
                    hashtag_counter[clean_tag] += 1

        top_5_hashtags = hashtag_counter.most_common(5)
        top_hashtags_list = []
        for hashtag, _ in top_5_hashtags:
            top_hashtags_list.append({
                "hashtag": hashtag,
                "channel_categories": sorted(list(hashtag_provinces[hashtag]))
            })

        # ساخت داده‌های نهایی
        data = {
            'total_posts': total_posts,
            'unique_users': unique_users,
            'total_views': total_views,
            'total_likes': total_likes,
            'daily_trend': [daily_trend],
            'view_trend': [view_trend],
            'like_trend': [like_trend],
            'top_hashtags': top_hashtags_list  # ✅ اضافه شده
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
        # data = [
        #     [f"{stat['province__name_en']}", stat['post_count']]
        #     for stat in province_stats
        # ]

        all_provinces = {
            "ardabil": 0,
            "isfahan": 0,
            "alborz": 0,
            "ilam": 0,
            "eastAzerbaijan": 0,
            "westAzerbaijan": 0,
            "bushehr": 0,
            "tehran": 0,
            "chaharmahalandBakhtiari": 0,
            "southKhorasan": 0,
            "razaviKhorasan": 0,
            "northKhorasan": 0,
            "khuzestan": 0,
            "zanjan": 0,
            "semnan": 0,
            "sistanAndBaluchestan": 0,
            "fars": 0,
            "qazvin": 0,
            "qom": 0,
            "kurdistan": 0,
            "kerman": 0,
            "kohgiluyehAndBoyerAhmad": 0,
            "kermanshah": 0,
            "golestan": 0,
            "gilan": 0,
            "lorestan": 0,
            "mazandaran": 0,
            "markazi": 0,
            "hormozgan": 0,
            "hamadan": 0,
            "yazd": 0,
        }

        # به روزرسانی مقادیر
        for stat in province_stats:
            province_name = stat['province__name_en']
            # تبدیل نام استان به فرمت camelCase اگر لازم است
            if province_name in all_provinces:
                all_provinces[province_name] = stat['post_count']

        return Response(all_provinces)

        # return Response(data)

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
            "#A281DD", "#FB7979", "#69AAD1", "#d98a5e", "#f0a582",
            "#c16a43", "#a55a3a", "#e57e4d", "#A281DD", "#b85e38"
        ]

    categories = []
    data = []

    for idx, item in enumerate(queryset):
        username = item[name_field]
        value = item[value_field]

        categories.append(username)
        color = colors[idx % len(colors)]
        data.append({"y": value, "color": color})

    return [{
        "categories": categories,
        "data": data
    }]




def prepare_pie_series(data_list, name_field, count_field, colors=None):
    """
    تبدیل لیست داده به فرمت سری نمودار (مثل pie یا bar)
    """
    if colors is None:
        colors = [
            "#69AAD1", "#A281DD", "#FB7979", "#d98a5e", "#f0a582",
            "#c16a43", "#a55a3a", "#e57e4d", "#FB7979", "#b85e38"
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

        # آمار کلی از داده‌های فیلتر شده کاربر
        total_posts = queryset.count()
        total_likes = queryset.aggregate(total=Coalesce(Sum('like_count'), 0))['total'] or 0
        total_views = queryset.aggregate(total=Coalesce(Sum('view_count'), 0))['total'] or 0

        # محاسبه درصد نسبت به کل داده‌های بدون فیلتر دسترسی کاربر
        if request.user.is_superuser:
            # برای سوپر یوزر، کل داده‌های سیستم
            all_posts_count = Post.objects.all().count() or 1
            all_likes = Post.objects.all().aggregate(total=Coalesce(Sum('like_count'), 0))['total'] or 1
            all_views = Post.objects.all().aggregate(total=Coalesce(Sum('view_count'), 0))['total'] or 1
        else:
            # برای کاربران عادی، کل داده‌هایی که دسترسی دارند
            user_provinces = UserProvinceAccess.objects.filter(user=request.user).values_list('province_id', flat=True)
            all_user_posts = Post.objects.filter(province_id__in=user_provinces)

            all_posts_count = all_user_posts.count() or 1
            all_likes = all_user_posts.aggregate(total=Coalesce(Sum('like_count'), 0))['total'] or 1
            all_views = all_user_posts.aggregate(total=Coalesce(Sum('view_count'), 0))['total'] or 1

        # محاسبه درصدها
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

        # کاربران موثر و فعال - بر اساس ترکیب کانال و پلتفرم
        top_users_by_likes_qs = (queryset.exclude(channel__isnull=True)
                                     .values('channel__name_fa', 'platform__name')  # تغییر به platform__name
                                     .annotate(total_likes=Sum('like_count'))
                                     .order_by('-total_likes')[:20])

        top_users_by_likes = []
        categories_likes = []
        data_likes = []
        for user in top_users_by_likes_qs:
            display_name = f"{user['channel__name_fa']} ({user['platform__name']})"  # استفاده از platform__name
            categories_likes.append(display_name)
            data_likes.append({
                'y': user['total_likes'],
                'color': '#A281DD'
            })

        if categories_likes and data_likes:
            top_users_by_likes.append({
                'categories': categories_likes,
                'data': data_likes
            })

        top_users_by_views_qs = (queryset.exclude(channel__isnull=True)
                                     .values('channel__name_fa', 'platform__name')  # تغییر به platform__name
                                     .annotate(total_views=Sum('view_count'))
                                     .order_by('-total_views')[:20])

        top_users_by_views = []
        categories_views = []
        data_views = []
        for user in top_users_by_views_qs:
            display_name = f"{user['channel__name_fa']} ({user['platform__name']})"  # استفاده از platform__name
            categories_views.append(display_name)
            data_views.append({
                'y': user['total_views'],
                'color': '#A281DD'
            })

        if categories_views and data_views:
            top_users_by_views.append({
                'categories': categories_views,
                'data': data_views
            })

        active_users_qs = (queryset.exclude(channel__isnull=True)
                               .values('channel__name_fa', 'platform__name')  # تغییر به platform__name
                               .annotate(post_count=Count('id'))
                               .order_by('-post_count')[:20])

        active_users = []
        categories_active = []
        data_active = []
        for user in active_users_qs:
            display_name = f"{user['channel__name_fa']} ({user['platform__name']})"  # استفاده از platform__name
            categories_active.append(display_name)
            data_active.append({
                'y': user['post_count'],
                'color': '#A281DD'
            })

        if categories_active and data_active:
            active_users.append({
                'categories': categories_active,
                'data': data_active
            })

        # فعالترین کانال‌ها - با پلتفرم
        active_channels_qs = (queryset.exclude(channel__isnull=True)
                                  .values('channel__name_fa', 'platform__name')  # تغییر به platform__name
                                  .annotate(post_count=Count('id'))
                                  .order_by('-post_count')[:10])

        active_channels = []
        for channel in active_channels_qs:
            display_name = f"{channel['channel__name_fa']} ({channel['platform__name']})"  # استفاده از platform__name
            active_channels.append({
                'name': display_name,
                'y': channel['post_count'],
                'color': '#69AAD1'
            })

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
                'name': stat['sentiment'],
                'y': stat['count'],
                'percentage': round(percentage, 2),
                "color": "#69AAD1"
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
        dates_gregorian = [today - timedelta(days=i) for i in range(13, -1, -1)]

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
                'borderWidth': 0.5,
                'data': heatmap_data
            }]
        }

        # فعالترین برنامه‌ها - بر اساس تعداد پست
        active_tv_programs_qs = (queryset.exclude(tv_program__isnull=True)
                                     .values('tv_program__name')
                                     .annotate(post_count=Count('id'))
                                     .order_by('-post_count')[:10])

        active_tv_programs = []
        categories_programs_posts = []
        data_programs_posts = []
        for program in active_tv_programs_qs:
            categories_programs_posts.append(program['tv_program__name'])
            data_programs_posts.append({
                'y': program['post_count'],
                'color': '#A281DD'
            })

        if categories_programs_posts and data_programs_posts:
            active_tv_programs.append({
                'categories': categories_programs_posts,
                'data': data_programs_posts
            })

        # پربازدیدترین برنامه‌ها - بر اساس مجموع بازدید
        top_viewed_tv_programs_qs = (queryset.exclude(tv_program__isnull=True)
                                         .values('tv_program__name')
                                         .annotate(total_views=Sum('view_count'))
                                         .order_by('-total_views')[:10])

        top_viewed_tv_programs = []
        categories_programs_views = []
        data_programs_views = []
        for program in top_viewed_tv_programs_qs:
            categories_programs_views.append(program['tv_program__name'])
            data_programs_views.append({
                'y': program['total_views'],
                'color': '#A281DD'
            })

        if categories_programs_views and data_programs_views:
            top_viewed_tv_programs.append({
                'categories': categories_programs_views,
                'data': data_programs_views
            })

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
            'topics_heatmap': topics_heatmap,
            'active_tv_programs': active_tv_programs,
            'top_viewed_tv_programs': top_viewed_tv_programs,
        }

        return Response(data)