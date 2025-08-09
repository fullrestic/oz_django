from datetime import datetime

from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from blog.models import Blog, Comment
from blog.serializers import BlogSerializer, CommentSerializer, CommentUpdateSerializer
from utils.permissions import IsAuthorOrReadOnly


class BlogQuerySetMixin :
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # pagination_class는 settings에 등록한 default pagination class가 들어가서 안 적어줘도 됨

    def get_queryset(self):
        return self.queryset.filter(
            Q(published_at__isnull=True) |
            Q(published_at__gte=timezone.now())
        ).order_by('-created_at').select_related('author')


class BlogListAPIView(BlogQuerySetMixin, ListCreateAPIView) :
    # 블로그 생성시 author 부분 넣어서 저장해주기
    # generics에서는 perform_create에서 save를 진행해주기 때문에 해당 메서드 수정
    def perform_create(self, serializer) :
        serializer.save(author=self.request.user)


class BlogRetrieveUpdateDestroyAPIView(BlogQuerySetMixin, RetrieveUpdateDestroyAPIView) :
    # 작성자와 같을 때만 수행되도록 Permission class 변경
    permission_classes = [IsAuthorOrReadOnly]




class CommentListCreateAPIView(ListCreateAPIView) :
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer) :
        blog = self.get_blog_object()
        serializer.save(author=self.request.user, blog=blog)

    def get_queryset(self):
        queryset = super().get_queryset()
        blog = self.get_blog_object()
        return queryset.filter(blog=blog)

    def get_blog_object(self):
        return get_object_or_404(Blog, pk=self.kwargs.get('blog_pk'))


class CommentUpdateDestroyAPIView(UpdateAPIView, DestroyAPIView) :
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    permission_classes = [IsAuthorOrReadOnly]
