from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render
from requests import Response

from rest_framework.decorators import permission_classes, action, api_view
from rest_framework import status, viewsets, filters
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .filter import TitleFilter
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import (filters, mixins, status, permissions,
                            viewsets)
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from reviews.models import *
from api.serializers import CommentSerializer
from .permissions import  AllowAny, AdminOnly
from .serializers import *
from .serializers import (AdminUserSerializer, CategoriesSerializer,
                         CommentSerializer, GenresSerializer,
                         GetTokenSerializer, RegisterSerializer,
                         ReviewSerializer, TitleSerializer, 
                         UserSerializer, SignUpSerializer)
from .permissions import (IsAdminOrReadOnlyAnonymusPermission, 
                          ReviewAndCommentPermission, OnlyAdmin)


@permission_classes([IsAuthenticated & AdminOnly])
class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)

class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (permissions.IsAuthenticated, OnlyAdmin)
    pagination_class = PageNumberPagination

    @action(
        methods=['get', 'patch', 'delete'],
        detail=False,
        url_path=r'(?P<username>\w+)'
    )
    def admin_functions(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.method == 'GET':
            serializer = AdminUserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            data = request.data.copy()
            data['username'] = user.username
            data['email'] = user.email
            serializer = AdminUserSerializer(user, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


class APIGetToken(APIView):

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь не найден'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class APISignup(APIView):

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            f'Спасибо за регистрацию, {user.username}.'
            f'\nКод подтвержения для доступа к API: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтвержения для доступа к API'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetListCreateDeleteViewSet(mixins.ListModelMixin,
                                 mixins.CreateModelMixin,
                                 mixins.DestroyModelMixin,
                                 viewsets.GenericViewSet):
    pass


class GenresViewSet(GetListCreateDeleteViewSet):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    serializer_class = GenresSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnlyAnonymusPermission,)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminOrReadOnlyAnonymusPermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter


class CategoriesViewSet(GetListCreateDeleteViewSet):
    lookup_field = 'slug'
    queryset = Category.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    serializer_class = CategoriesSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnlyAnonymusPermission,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (ReviewAndCommentPermission,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        if not Review.objects.filter(id=review_id).exists():
            raise NotFound()
        review = Review.objects.get(id=review_id)
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        if not Review.objects.filter(id=review_id).exists():
            raise NotFound()
        return Comment.objects.filter(review=review_id)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (ReviewAndCommentPermission,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        if not Title.objects.filter(id=title_id).exists():
            raise NotFound()
        title = Title.objects.get(id=title_id)
        existing = Review.objects.filter(
            author=self.request.user,
            title=title
        ).exists()
        if existing:
            raise ParseError()
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        if get_object_or_404(Title, pk=title_id):
            return Review.objects.filter(title=title_id)

