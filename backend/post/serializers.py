from rest_framework import serializers
from django.contrib.auth import get_user_model

from core.models import Category, Post, Comment, Restaurant


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category object"""

    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)


class PostUserSerializer(serializers.ModelSerializer):
    """Serializer for addressing a user of the post"""

    class Meta:
        model = get_user_model()
        fields = ('username', )  # will add 'profile_pic'


class PostSerializer(serializers.ModelSerializer):
    """Serializer for post object"""
    user = PostUserSerializer(read_only=True)
    restaurant = serializers.SerializerMethodField()
    number_of_comments = serializers.SerializerMethodField()
    post_comments = serializers.SerializerMethodField()
    liked_by_req_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'user', 'note', 'posted_on', 'restaurant',
                  'number_of_likes', 'number_of_comments',
                  'post_comments', 'liked_by_req_user')
        read_only_fields = ('id',)

    def get_restaurant(self, obj):
        serializer = RestaurantSerializer(
            obj.post_restaurant.all(), many=True)

        return serializer.data

    def get_number_of_comments(self, obj):
        return Comment.objects.filter(post=obj).count()

    def get_post_comments(self, obj):
        post_comments = obj.post_comments.all()
        serializer = CommentSerializer(post_comments, many=True)

        return serializer.data

    def get_liked_by_req_user(self, obj):
        user = self.context['request'].user
        return user in obj.likes.all()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment object"""

    user = PostUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'comment_body', 'posted_on')
        read_only_fields = ('user', 'id', 'posted_on')


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer for restauran object"""
    post = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Post.objects.all()
    )
    category = CategorySerializer()

    class Meta:
        model = Restaurant
        fields = ('id', 'post', 'category', 'image', 'name', 'area',
                  'address', 'dish', 'expense', 'rating')
        read_only_fields = ('id',)


class RestaurantImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to restaurants"""

    class Meta:
        model = Restaurant
        fields = ('id', 'image')
        read_only_fields = ('id',)
