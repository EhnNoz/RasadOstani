from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta, datetime, date
from .models import Post, Platform, Province, UserProvinceAccess, Channel, UserCategory, PoliticalCategory, NewsType, \
    NewsTopic, Profile, TvProgram, DefineChannel, DefineTvProgram, DefineProfile, AboutUs
from .serializers import PostSerializer, PlatformSerializer, ProvinceSerializer, UserProvinceAccessSerializer, \
    ChannelSerializer, UserCategorySerializer, PoliticalCategorySerializer, NewsTypeSerializer, NewsTopicSerializer, \
    ProfileWithLatestPostsSerializer, ProfileListSerializer, TvProgramSerializer, CurrentUserSerializer, \
    AddChannelSerializer, AddTvProgramSerializer, AddProfileSerializer, AboutUsSerializer
from .filters import PostFilter, ProvinceStatsFilter, ChannelFilter, ProvinceFilter, ProfileFilter, TvProgramFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
import jdatetime
from jdatetime import date as jdate
from django.db.models import Count, Sum, Avg, F, ExpressionWrapper, FloatField
from django.db.models.functions import Coalesce
from collections import Counter, defaultdict
import re
from .permissions import HasProvinceAccess
import json
import hashlib
from django.core.cache import cache

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

    def _get_cache_key(self, request, view_name, extra_parts=None):
        """تولید کلید کش منحصربه‌فرد بر اساس کاربر، view و پارامترها"""
        parts = [str(request.user.id), view_name]
        if extra_parts:
            parts.extend(str(p) for p in extra_parts)
        # اضافه کردن query_params به صورت مرتب‌شده
        if hasattr(request, 'query_params'):
            params = dict(sorted(request.query_params.items()))
            parts.append(json.dumps(params, sort_keys=True, default=str))
        key_str = "|".join(parts)
        return hashlib.md5(key_str.encode('utf-8')).hexdigest()

    def _invalidate_cache_for_user(self, user_id):
        """پاک کردن هوشمند کش نیازمند استراتژی؛ در اینجا ما فقط همه کش‌های مرتبط را نمی‌توانیم پاک کنیم.
        به جای آن، در عملیات نوشتن (create/update/delete) کل کش را flush نمی‌کنیم، بلکه فقط در صورت نیاز دستی پاک می‌کنیم.
        برای سادگی، ما فقط کش‌های مرتبط با `list` و `statistics` را نمی‌توانیم پاک کنیم — پس timeout کوتاه می‌ذاریم.
        اگر نیاز به پاک کردن دقیق داری، باید از الگوی دیگری استفاده کنی."""
        pass  # در این پیاده‌سازی، از timeout استفاده می‌کنیم

    def _get_filtered_queryset(self, request):
        user = request.user
        if user.is_superuser:
            queryset = Post.objects.all()
        else:
            user_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province_id', flat=True)
            queryset = Post.objects.filter(province_id__in=user_provinces)
        post_filter = PostFilter(request.query_params, queryset=queryset)
        return post_filter.qs

    def _remove_duplicate_posts(self, queryset):
        """
        حذف پست‌های تکراری بر اساس تاریخ ایجاد، کانال و پلتفرم
        و انتخاب پستی با بیشترین بازدید
        """
        from django.db.models import OuterRef, Subquery

        # زیرکوئری برای پیدا کردن پست با بیشترین بازدید در هر گروه
        max_view_subquery = queryset.filter(
            datetime_create=OuterRef('datetime_create'),
            channel_id=OuterRef('channel_id'),
            platform_id=OuterRef('platform_id')
        ).order_by('-view_count').values('id')[:1]

        # فقط پست‌هایی که دارای بیشترین بازدید در گروه خود هستند را نگه داریم
        return queryset.filter(id=Subquery(max_view_subquery))

    def list(self, request):
        cache_key = self._get_cache_key(request, 'post_list')
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        # ✅ این خط، جستجوی Full-Text را از طریق PostFilter اعمال می‌کند
        queryset = self._get_filtered_queryset(request)

        # 🔥 اعمال فیلتر حذف داپلیکیت‌ها
        queryset = self._remove_duplicate_posts(queryset)

        sort_by = request.query_params.get('sort_by', 'newest')
        if sort_by == 'likes':
            queryset = queryset.order_by('-like_count')[:20]
        elif sort_by == 'views':
            queryset = queryset.order_by('-view_count')[:20]
        else:  # 'newest' or default
            queryset = queryset.order_by('-datetime_create')[:20]

        serializer = PostSerializer(queryset, many=True)
        data = serializer.data

        cache.set(cache_key, data, timeout=5 * 60)
        return Response(data)

    def retrieve(self, request, pk=None):
        cache_key = self._get_cache_key(request, 'post_retrieve', extra_parts=[pk])
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

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
            data = serializer.data
            cache.set(cache_key, data, timeout=10 * 60)  # 10 دقیقه
            return Response(data)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # --- عملیات‌های نوشتن: بدون کش، ولی می‌توانیم در آینده کش را پاک کنیم ---
    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # اگر بخواهی کش را پاک کنی، اینجا می‌توانی یک signal یا cache.delete_many() اجرا کنی
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
        return self.update(request, pk)  # ساده‌سازی

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
        cache_key = self._get_cache_key(request, 'post_statistics')
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        queryset = self._get_filtered_queryset(request)

        # 🔥 اعمال فیلتر حذف داپلیکیت‌ها
        queryset = self._remove_duplicate_posts(queryset)

        total_posts = queryset.count()
        unique_users = queryset.values('username').distinct().count()
        total_views = queryset.aggregate(total_views=Sum('view_count'))['total_views'] or 0
        total_likes = queryset.aggregate(total_likes=Sum('like_count'))['total_likes'] or 0

        daily_trend_qs = queryset.extra(
            select={'date': "DATE(datetime_create)"}
        ).values('date').annotate(
            posts=Count('id'),
            views=Sum('view_count'),
            likes=Sum('like_count')
        ).order_by('date')

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
                daily_categories.append(jalali_str)
                daily_post_data.append(item['posts'])
                daily_view_data.append(item['views'])
                daily_like_data.append(item['likes'])
            except (ValueError, OverflowError):
                continue

        daily_trend = {"name": "روند روزانه پست‌ها", "categories": daily_categories, "data": daily_post_data,
                       "color": "#A281DD"}
        view_trend = {"name": "روند بازدیدها", "categories": daily_categories, "data": daily_view_data, "color": "#A281DD"}
        like_trend = {"name": "روند لایک‌ها", "categories": daily_categories, "data": daily_like_data, "color": "#A281DD"}

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

        top_5_hashtags = hashtag_counter.most_common(3)
        top_hashtags_list = []
        for hashtag, _ in top_5_hashtags:
            top_hashtags_list.append({
                "hashtag": hashtag,
                "channel_categories": sorted(list(hashtag_provinces[hashtag]))
            })

        data = {
            'total_posts': total_posts,
            'unique_users': unique_users,
            'total_views': total_views,
            'total_likes': total_likes,
            'daily_trend': [daily_trend],
            'view_trend': [view_trend],
            'like_trend': [like_trend],
            'top_hashtags': top_hashtags_list
        }

        cache.set(cache_key, data, timeout=1 * 6)  # 10 دقیقه
        return Response(data)


class ProvinceStatsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def _get_cache_key(self, request):
        """تولید کلید کش منحصربه‌فرد بر اساس کاربر و query_params"""
        user_id = request.user.id
        params = dict(sorted(request.query_params.items()))
        params_str = json.dumps(params, sort_keys=True, default=str)
        key_str = f"province_stats_user_{user_id}_params_{params_str}"
        return hashlib.md5(key_str.encode('utf-8')).hexdigest()

    def _get_filtered_queryset(self, request):
        user = request.user
        if user.is_superuser:
            queryset = Post.objects.all()
        else:
            user_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province_id', flat=True)
            queryset = Post.objects.filter(province_id__in=user_provinces)

        stats_filter = ProvinceStatsFilter(request.query_params, queryset=queryset)
        return stats_filter.qs

    def _remove_duplicate_posts(self, queryset):
        """
        حذف پست‌های تکراری بر اساس تاریخ ایجاد، کانال و پلتفرم
        و انتخاب پستی با بیشترین بازدید
        """
        from django.db.models import OuterRef, Subquery

        # زیرکوئری برای پیدا کردن پست با بیشترین بازدید در هر گروه
        max_view_subquery = queryset.filter(
            datetime_create=OuterRef('datetime_create'),
            channel_id=OuterRef('channel_id'),
            platform_id=OuterRef('platform_id')
        ).order_by('-view_count').values('id')[:1]

        # فقط پست‌هایی که دارای بیشترین بازدید در گروه خود هستند را نگه داریم
        return queryset.filter(id=Subquery(max_view_subquery))

    def list(self, request):
        cache_key = self._get_cache_key(request)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        # ---- شروع محاسبات اصلی ----
        queryset = self._get_filtered_queryset(request)

        # 🔥 اعمال فیلتر حذف داپلیکیت‌ها
        queryset = self._remove_duplicate_posts(queryset)

        start_date_param = request.query_params.get('start_date')
        end_date_param = request.query_params.get('end_date')

        if not start_date_param and not end_date_param:
            default_end_date = timezone.now()
            default_start_date = default_end_date - timedelta(days=120)
            queryset = queryset.filter(
                datetime_create__range=(default_start_date, default_end_date)
            )

        province_stats = queryset.values(
            'province__name_en',
            'province__name_fa',
            'province__code'
        ).annotate(
            post_count=Count('id')
        ).order_by('-post_count')

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

        for stat in province_stats:
            province_name = stat['province__name_en']
            if province_name in all_provinces:
                all_provinces[province_name] = stat['post_count']

        # ذخیره در کش برای 10 دقیقه
        cache.set(cache_key, all_provinces, timeout=1 * 6)

        return Response(all_provinces)
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

    def _remove_duplicate_posts(self, queryset):
        """
        حذف پست‌های تکراری بر اساس تاریخ ایجاد، کانال و پلتفرم
        و انتخاب پستی با بیشترین بازدید
        """
        from django.db.models import OuterRef, Subquery

        # زیرکوئری برای پیدا کردن پست با بیشترین بازدید در هر گروه
        max_view_subquery = queryset.filter(
            datetime_create=OuterRef('datetime_create'),
            channel_id=OuterRef('channel_id'),
            platform_id=OuterRef('platform_id')
        ).order_by('-view_count').values('id')[:1]

        # فقط پست‌هایی که دارای بیشترین بازدید در گروه خود هستند را نگه داریم
        return queryset.filter(id=Subquery(max_view_subquery))

    def _get_cache_key(self, request):
        """تولید کلید منحصربه‌فرد برای کش بر اساس کاربر و query_params"""
        user_id = request.user.id
        params = dict(sorted(request.query_params.items()))
        params_str = json.dumps(params, sort_keys=True, default=str)
        key_str = f"advanced_analytics_user_{user_id}_params_{params_str}"
        return hashlib.md5(key_str.encode('utf-8')).hexdigest()

    def list(self, request):
        cache_key = self._get_cache_key(request)
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        # === شروع محاسبات سنگین ===
        queryset = self._get_filtered_queryset(request)

        # 🔥 اعمال فیلتر حذف داپلیکیت‌ها
        queryset = self._remove_duplicate_posts(queryset)

        # آمار کلی از داده‌های فیلتر شده کاربر
        total_posts = queryset.count()
        total_likes = queryset.aggregate(total=Coalesce(Sum('like_count'), 0))['total'] or 0
        total_views = queryset.aggregate(total=Coalesce(Sum('view_count'), 0))['total'] or 0

        # محاسبه درصد نسبت به کل داده‌های بدون فیلتر دسترسی کاربر
        if request.user.is_superuser:
            all_posts = Post.objects.all()
        else:
            user_provinces = UserProvinceAccess.objects.filter(user=request.user).values_list('province_id',
                                                                                              flat=True)
            all_posts = Post.objects.filter(province_id__in=user_provinces)

        # 🔥 اعمال فیلتر حذف داپلیکیت‌ها روی all_posts هم
        all_posts = self._remove_duplicate_posts(all_posts)

        all_posts_count = all_posts.count() or 1
        all_likes = all_posts.aggregate(total=Coalesce(Sum('like_count'), 0))['total'] or 1
        all_views = all_posts.aggregate(total=Coalesce(Sum('view_count'), 0))['total'] or 1

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
        def serialize_top_users(qs, value_field, limit=20):
            categories = []
            data = []
            for item in qs[:limit]:
                display_name = f"{item['channel__name_fa']} ({item['platform__name']})"
                categories.append(display_name)
                data.append({'y': item[value_field], 'color': '#A281DD'})
            return [{'categories': categories, 'data': data}] if categories else []

        top_users_by_likes_qs = (
            queryset.exclude(channel__isnull=True)
            .values('channel__name_fa', 'platform__name')
            .annotate(total_likes=Sum('like_count'))
            .order_by('-total_likes')
        )
        top_users_by_likes = serialize_top_users(top_users_by_likes_qs, 'total_likes')

        top_users_by_views_qs = (
            queryset.exclude(channel__isnull=True)
            .values('channel__name_fa', 'platform__name')
            .annotate(total_views=Sum('view_count'))
            .order_by('-total_views')
        )
        top_users_by_views = serialize_top_users(top_users_by_views_qs, 'total_views')

        active_users_qs = (
            queryset.exclude(channel__isnull=True)
            .values('channel__name_fa', 'platform__name')
            .annotate(post_count=Count('id'))
            .order_by('-post_count')
        )
        active_users = serialize_top_users(active_users_qs, 'post_count')

        # فعالترین کانال‌ها - با پلتفرم
        active_channels_qs = (
            queryset.exclude(channel__isnull=True)
            .values('channel__name_fa', 'platform__name')
            .annotate(post_count=Count('id'))
            .order_by('-post_count')[:10]
        )
        active_channels = [
            {
                'name': f"{ch['channel__name_fa']} ({ch['platform__name']})",
                'y': ch['post_count'],
                'color': '#69AAD1'
            }
            for ch in active_channels_qs
        ]

        # توزیع کانال‌ها بر اساس نوع
        channel_type_stats = (
            queryset.exclude(channel__isnull=True)
            .values('channel__channel_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        channel_type_distribution = prepare_pie_series(
            list(channel_type_stats),
            name_field='channel__channel_type',
            count_field='count'
        )

        # فراوانی جریانات سیاسی
        # --- فراوانی جریانات سیاسی ---
        political_currents_raw = (
            queryset
                .exclude(channel__political_category__isnull=True)
                .values('channel__political_category__name')
                .annotate(
                post_count=Count('id'),
                total_likes=Sum('like_count'),
                total_views=Sum('view_count')
            )
        )

        # ✅ گروه‌بندی دستی بر اساس نام
        pc_grouped = defaultdict(int)
        for item in political_currents_raw:
            pc_grouped[item['channel__political_category__name']] += item['post_count']

        # مرتب‌سازی و محدود کردن به 15
        top_pc = sorted(pc_grouped.items(), key=lambda x: -x[1])[:15]
        political_currents_clean = [{'name': name, 'post_count': count} for name, count in top_pc]

        political_currents_distribution = prepare_pie_series(
            political_currents_clean,
            name_field='name',
            count_field='post_count'
        )

        # فراوانی گروه‌های کاربری
        user_groups_stats = (
            queryset.exclude(channel__user_category__isnull=True)
            .values('channel__user_category__name')
            .annotate(
                post_count=Count('id'),
                total_likes=Sum('like_count'),
                total_views=Sum('view_count')
            )
            .order_by('-post_count')[:15]
        )
        user_groups_distribution = prepare_pie_series(
            list(user_groups_stats),
            name_field='channel__user_category__name',
            count_field='post_count'
        )

        # فراوانی احساسات
        sentiment_stats = (
            queryset.values('sentiment')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
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
                jalali_date = jdatetime.fromgregorian(date=date)
                dates_categories.append(jalali_date.strftime("%Y-%m-%d"))
            except Exception:
                dates_categories.append(date.strftime("%Y-%m-%d"))

        # 🔥 استفاده از queryset اصلی به جای Post.objects.filter
        heatmap_queryset = self._get_filtered_queryset(request).filter(
            datetime_create__date__gte=dates_gregorian[0],
            datetime_create__date__lte=dates_gregorian[-1]
        )

        # 🔥 اعمال فیلتر حذف داپلیکیت‌ها روی هیت مپ
        heatmap_queryset = self._remove_duplicate_posts(heatmap_queryset)

        top_topics_qs = (
            heatmap_queryset
                .exclude(news_topic__isnull=True)
                .values('news_topic__id', 'news_topic__name')
                .annotate(count=Count('id'))
                .order_by('-count')[:10]
        )
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

        # فعالترین و پربازدیدترین برنامه‌های تلویزیونی
        def serialize_tv_programs(qs, value_field, limit=10):
            categories = []
            data = []
            for item in qs[:limit]:
                categories.append(item['tv_program__name'])
                data.append({'y': item[value_field], 'color': '#FB7979'})
            return [{'categories': categories, 'data': data}] if categories else []

        active_tv_programs_qs = (
            queryset.exclude(tv_program__isnull=True)
            .values('tv_program__name')
            .annotate(post_count=Count('id'))
            .order_by('-post_count')
        )
        active_tv_programs = serialize_tv_programs(active_tv_programs_qs, 'post_count')

        top_viewed_tv_programs_qs = (
            queryset.exclude(tv_program__isnull=True)
            .values('tv_program__name')
            .annotate(total_views=Sum('view_count'))
            .order_by('-total_views')
        )
        top_viewed_tv_programs = serialize_tv_programs(top_viewed_tv_programs_qs, 'total_views')

        # === ساخت دیکشنری نهایی ===
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

        # ذخیره در کش برای 15 دقیقه
        cache.set(cache_key, data, timeout=1 * 6)

        return Response(data)


class IsSuperUserOrProvinceAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        user_provinces = UserProvinceAccess.objects.filter(user=request.user).values_list('province_id', flat=True)
        return obj.province_id in user_provinces


class ProfileListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileListSerializer
    permission_classes = [IsSuperUserOrProvinceAccess]
    filterset_class = ProfileFilter
    ordering_fields = ['name', 'created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Profile.objects.all()
        user_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province_id', flat=True)
        return Profile.objects.filter(province_id__in=user_provinces)


class ProfileLatestPostsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileWithLatestPostsSerializer
    permission_classes = [IsSuperUserOrProvinceAccess]
    filterset_class = ProfileFilter

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Profile.objects.prefetch_related(
                'celebrities__posts__platform',
                'celebrities__platform'
            )
        user_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province_id', flat=True)
        return Profile.objects.filter(province_id__in=user_provinces).prefetch_related(
            'celebrities__posts__platform',
            'celebrities__platform'
        )

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CurrentUserViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CurrentUserSerializer

    def get_queryset(self):
        # فقط کاربر جاری رو برمی‌گردونیم
        return self.request.user.__class__.objects.filter(id=self.request.user.id)

    def get_object(self):
        # می‌تونیم اینجا هم کاربر جاری رو برگردونیم
        return self.request.user


class AddChannelViewSet(viewsets.ModelViewSet):
    serializer_class = AddChannelSerializer
    permission_classes = [IsAuthenticated, HasProvinceAccess]

    def get_queryset(self):
        # فقط کانال‌هایی که استانشان در دسترس کاربر است
        user = self.request.user
        accessible_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province', flat=True)
        return DefineChannel.objects.filter(province__in=accessible_provinces)

    def perform_create(self, serializer):
        # وقتی کاربر کانال اضافه می‌کند، مطمئن شویم که استان آن متعلق به دسترسی‌هایش باشد
        province = serializer.validated_data.get('province')
        if not UserProvinceAccess.objects.filter(user=self.request.user, province=province).exists():
            self.permission_denied(self.request, message="شما به این استان دسترسی ندارید.")
        serializer.save()


class AddTvProgramViewSet(viewsets.ModelViewSet):
    serializer_class = AddTvProgramSerializer
    permission_classes = [IsAuthenticated, HasProvinceAccess]

    def get_queryset(self):
        # فقط کانال‌هایی که استانشان در دسترس کاربر است
        user = self.request.user
        accessible_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province', flat=True)
        return DefineTvProgram.objects.filter(province__in=accessible_provinces)

    def perform_create(self, serializer):
        # وقتی کاربر کانال اضافه می‌کند، مطمئن شویم که استان آن متعلق به دسترسی‌هایش باشد
        province = serializer.validated_data.get('province')
        if not UserProvinceAccess.objects.filter(user=self.request.user, province=province).exists():
            self.permission_denied(self.request, message="شما به این استان دسترسی ندارید.")
        serializer.save()


class AddProfileViewSet(viewsets.ModelViewSet):
    serializer_class = AddProfileSerializer
    permission_classes = [IsAuthenticated, HasProvinceAccess]

    def get_queryset(self):
        # فقط کانال‌هایی که استانشان در دسترس کاربر است
        user = self.request.user
        accessible_provinces = UserProvinceAccess.objects.filter(user=user).values_list('province', flat=True)
        return DefineProfile.objects.filter(province__in=accessible_provinces)

    def perform_create(self, serializer):
        # وقتی کاربر کانال اضافه می‌کند، مطمئن شویم که استان آن متعلق به دسترسی‌هایش باشد
        province = serializer.validated_data.get('province')
        if not UserProvinceAccess.objects.filter(user=self.request.user, province=province).exists():
            self.permission_denied(self.request, message="شما به این استان دسترسی ندارید.")
        serializer.save()


class AboutUsView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AboutUsSerializer

    def get_object(self):
        # فقط اولین رکورد را برمی‌گرداند (چون منطقاً فقط یکی وجود دارد)
        return AboutUs.objects.first()





