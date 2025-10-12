from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import PostViewSet, PlatformViewSet, ProvinceViewSet, UserProvinceAccessViewSet, ProvinceStatsViewSet, \
    AdvancedAnalyticsViewSet, ChannelViewSet, PoliticalCategoryViewSet, UserCategoryViewSet

router = DefaultRouter()
router.register(r'platforms', PlatformViewSet, basename='platform')
router.register(r'provinces', ProvinceViewSet, basename='province')
router.register(r'user-province-access', UserProvinceAccessViewSet, basename='userprovinceaccess')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'province-stats', ProvinceStatsViewSet, basename='provincestats')
router.register(r'channels', ChannelViewSet, basename='channel')
router.register(r'political-categories', PoliticalCategoryViewSet, basename='politicalcategory')
router.register(r'user-categories', UserCategoryViewSet, basename='usercategory')
router.register(r'advanced-analytics', AdvancedAnalyticsViewSet, basename='advancedanalytics')


urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]