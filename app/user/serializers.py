from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from core.models import Post, Comment

from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for creating a new user account"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True,
                                     'min_length': 5},
                        'username': {'min_length': 3}}

    def create(self, validated_data):
        """Create a new use with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class UserInfoSerializer(serializers.ModelSerializer):
    """Serializer for the user settings objects"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password', 'bio')
        extra_kwargs = {'password': {'write_only': True,
                                     'min_length': 5},
                        'username': {'min_length': 3}}

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class UserPostSerializer(serializers.ModelSerializer):
    """Serializer for viewing a user profile and posts"""
    number_of_comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'posted_on', 'note',
                  'number_of_likes', 'number_of_comments')

    def get_number_of_comments(self, obj):
        return Comment.objects.filter(post=obj).count()


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing a user posts"""
    number_of_posts = serializers.SerializerMethodField()
    followed_by_req_user = serializers.SerializerMethodField()
    user_posts = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'bio', 'number_of_followers',
                  'number_of_following', 'number_of_posts',
                  'user_posts', 'followed_by_req_user')

    def get_number_of_posts(self, obj):
        return Post.objects.filter(user=obj).count()

    def get_user_posts(self, obj):
        serializer = UserPostSerializer(obj.user_posts.all(), many=True)

        return serializer.data

    def get_followed_by_req_user(self, obj):
        user = self.context['request'].user

        return user in obj.followers.all()


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for listing all followers"""

    class Meta:
        model = get_user_model()
        fields = '__all__'
