from rest_framework import serializers

from core.models import Category, Post, Comment


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
    """Serializer for creating comments"""

    post = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Post.objects.all()
    )

    class Meta:
        model = Comment
        fields = ('id', 'user', 'post', 'comment_body')
        read_only_fields = ('id', 'user', 'post')
