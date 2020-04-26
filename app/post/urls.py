from django.urls import path, include
from rest_framework.routers import DefaultRouter

from post import views


router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('posts', views.PostViewSet)
# router.register('comments', views.CommentViewSet)
router.register('restaurants', views.RestaurantViewSet)


app_name = 'post'

urlpatterns = [
    path('', include(router.urls)),
    path('comment/<uuid:post_id>/',
         views.CommentAddView.as_view(), name='add-comment'),
    path('comment/<int:comment_id>/',
         views.CommentManagerView.as_view(), name='manage-comment'),
    path('like/<uuid:post_id>/', views.LikeView.as_view(), name='like'),
    path('<uuid:post_id>/get-likers/',
         views.GetLikersView.as_view(), name='get-likers'),
]
