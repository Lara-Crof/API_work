from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (APIGetToken, APISignup, UsersViewSet, CategoriesViewSet, CommentViewSet, GenresViewSet,
                                                          ReviewViewSet, TitlesViewSet)
app_name = 'api'

v1_router = SimpleRouter()

v1_router.register(
    'users',
    UsersViewSet,
    basename='users'
)
v1_router.register(
    r'titles', TitlesViewSet, basename='titles'
)
v1_router.register(
    r'genres', GenresViewSet, basename='genres'
)
v1_router.register(
    r'categories', CategoriesViewSet, basename='categories'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet, basename='reviews'
)
v1_router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', APISignup.as_view(), name='signup'),
]
