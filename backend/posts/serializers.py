from rest_framework import serializers
from .models import Post, Platform, Province, UserProvinceAccess, Channel, PoliticalCategory, UserCategory, NewsType, \
    NewsTopic
from django.contrib.auth.models import User


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name_fa', 'name_en','code','province_query']


class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ['id', 'name', 'description']


class NewsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsType
        fields = '__all__'


class NewsTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTopic
        fields = '__all__'

class PoliticalCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PoliticalCategory
        fields = '__all__'


class UserCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCategory
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    province_name_fa = serializers.CharField(source='province.name_fa', read_only=True)
    province_name_en = serializers.CharField(source='province.name_en', read_only=True)

    # فیلدهای جدید مربوط به کانال
    channel_username = serializers.CharField(source='channel.username', read_only=True)
    channel_type = serializers.CharField(source='channel.channel_type', read_only=True)
    channel_main_category = serializers.CharField(source='channel.main_category', read_only=True)
    channel_sub_category = serializers.CharField(source='channel.sub_category', read_only=True)
    channel_platform_name = serializers.CharField(source='channel.platform.name', read_only=True)

    news_type_name = serializers.CharField(source='news_type.name', read_only=True)
    news_topic_name = serializers.CharField(source='news_topic.name', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class UserProvinceAccessSerializer(serializers.ModelSerializer):
    province_name_fa = serializers.CharField(source='province.name_fa', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProvinceAccess
        fields = ['id', 'user', 'username', 'province', 'province_name_fa']


class UserSerializer(serializers.ModelSerializer):
    provinces = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'provinces']

    def get_provinces(self, obj):
        access_list = UserProvinceAccess.objects.filter(user=obj)
        return [access.province.name_fa for access in access_list]


class ProvinceStatsSerializer(serializers.Serializer):
    province_name_en = serializers.CharField()
    province_name_fa = serializers.CharField()
    post_count = serializers.IntegerField()


# class PoliticalCurrentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PoliticalCurrent
#         fields = '__all__'
#
#
# class UserGroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserGroup
#         fields = '__all__'


class ChannelSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    political_category_name = serializers.CharField(source='political_category.name', read_only=True)
    user_category_name = serializers.CharField(source='user_category.name', read_only=True)
    main_category = serializers.SerializerMethodField()

    class Meta:
        model = Channel
        fields = '__all__'

    def get_main_category(self, obj):
        return obj.get_main_category()


class PostSerializer(serializers.ModelSerializer):
    platform_name = serializers.CharField(source='platform.name', read_only=True)
    province_name_fa = serializers.CharField(source='province.name_fa', read_only=True)
    province_name_en = serializers.CharField(source='province.name_en', read_only=True)

    # فیلدهای جدید مربوط به کانال
    channel_name_fa = serializers.CharField(source='channel.name_fa', read_only=True)
    channel_username = serializers.CharField(source='channel.username', read_only=True)
    channel_type = serializers.CharField(source='channel.channel_type', read_only=True)
    channel_political_category = serializers.CharField(source='channel.political_category.name', read_only=True)
    channel_user_category = serializers.CharField(source='channel.user_category.name', read_only=True)
    channel_main_category = serializers.SerializerMethodField()

    news_type_name = serializers.CharField(source='news_type.name', read_only=True)
    news_topic_name = serializers.CharField(source='news_topic.name', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

    def get_channel_main_category(self, obj):
        if obj.channel:
            return obj.channel.get_main_category()
        return None

