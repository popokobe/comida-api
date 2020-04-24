from rest_framework import serializers

from core.models import Category, Post, Comment, Restaurant


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category object"""

    class Meta:
        model = Category
        fields = ('id', 'name')
        read_only_fields = ('id',)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for post object"""

    class Meta:
        model = Post
        fields = ('id', 'title', 'note')
        read_only_fields = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for comment object"""

    post = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Post.objects.all()
    )

    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'comment_body')
        read_only_fields = ('id', 'user', 'post')


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer for restauran object"""
    post = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Post.objects.all()
    )
    category = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Category.objects.all()
    )

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
