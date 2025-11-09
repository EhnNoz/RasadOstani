from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import PostViewSet, PlatformViewSet, ProvinceViewSet, UserProvinceAccessViewSet, ProvinceStatsViewSet, \
    AdvancedAnalyticsViewSet, ChannelViewSet, PoliticalCategoryViewSet, UserCategoryViewSet, NewsTypeViewSet, \
    NewsTopicViewSet, ProfileListViewSet, ProfileLatestPostsViewSet, CurrentUserViewSet, AddChannelViewSet, \
    AddTvProgramViewSet, AddProfileViewSet, AboutUsView

router = DefaultRouter()
router.register(r'platforms', PlatformViewSet, basename='platform')
router.register(r'news-type', NewsTypeViewSet, basename='newstype')
router.register(r'news-topic', NewsTopicViewSet, basename='newstopic')
router.register(r'provinces', ProvinceViewSet, basename='province')
router.register(r'user-province-access', UserProvinceAccessViewSet, basename='userprovinceaccess')
router.register(r'posts', PostViewSet, basename='post')
router.register(r'province-stats', ProvinceStatsViewSet, basename='provincestats')
router.register(r'channels', ChannelViewSet, basename='channel')
router.register(r'political-categories', PoliticalCategoryViewSet, basename='politicalcategory')
router.register(r'user-categories', UserCategoryViewSet, basename='usercategory')
router.register(r'advanced-analytics', AdvancedAnalyticsViewSet, basename='advancedanalytics')
router.register(r'profiles', ProfileListViewSet, basename='profile-list')
router.register(r'profiles-with-posts', ProfileLatestPostsViewSet, basename='profile-with-posts')
router.register('current-user', CurrentUserViewSet, basename='current-user')
router.register(r'add-channels', AddChannelViewSet, basename='add-channels')
router.register(r'add-tvprogram', AddTvProgramViewSet, basename='add-tvprogram')
router.register(r'add-profile', AddProfileViewSet, basename='add-profile')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('about-us/', AboutUsView.as_view(), name='about-us'),

]