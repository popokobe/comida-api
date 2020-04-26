from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, mixins, status, generics
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from core.models import Category, Post, Comment, Restaurant

from post import serializers


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin):
    """Manage categories in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new category"""
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    """Manage posts in the databese"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user) \
            .order_by('-posted_on')

    def perform_create(self, serializer):
        """Create a new post"""
        serializer.save(user=self.request.user)


class CommentAddView(generics.CreateAPIView):
    """View just for creating a new comment"""
    serializer_class = serializers.CommentSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, post_id=None):
        post = Post.objects.get(pk=post_id)
        serializer = serializers.CommentSerializer(data=request.data)

        if serializer.valid():
            serializer.save(post=post, user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )


class CommentManagerView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CommentSerializer
    lookup_url_kwarg = 'comment_id'

    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset


# class CommentViewSet(viewsets.GenericViewSet,
#                      mixins.ListModelMixin,
#                      mixins.CreateModelMixin):
#     """Manage comments in the database"""
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     queryset = Comment.objects.all()
#     serializer_class = serializers.CommentSerializer

#     def perform_create(self, serializer):
#         """Create a new comment"""
#         serializer.save(user=self.request.user)


class LikeView(APIView):
    """Toggle like"""

    def get(self, request, format=None, post_id=None):
        post = Post.objects.get(pk=post_id)
        user = self.request.user
        if user.is_authenticated:
            if user in post.likes.all():
                like = False
                post.likes.remove(user)
            else:
                like = True
                post.likes.add(user)
        data = {
            'likes': like
        }
        return Response(data)


class GetLikersView(generics.ListAPIView):
    serializer_class = serializers.PostUserSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        queryset = Post.objects.get(
            pk=post_id).likes.all()
        return queryset


class RestaurantViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Restaurant.objects.all()
    serializer_class = serializers.RestaurantSerializer

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'upload_image':
            return serializers.RestaurantImageSerializer

        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a restaurant"""
        restaurant = self.get_object()
        serializer = self.get_serializer(
            restaurant,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
