from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, schema
from rest_framework.schemas import AutoSchema
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.http.response import Http404
from django.shortcuts import get_object_or_404

from blog.models import Blog
from blog.serializers import BlogSerializer
from utils.permissions import IsAuthorOrReadOnly


class BlogListCreateAPIView(APIView) :
    # LoginRequiredMixin사용 불가! permission_classes로 처리해줘야 함
    permission_classes = [IsAuthenticatedOrReadOnly]
        # IsAuthenticated : GET요청 할 때도 체크가 됨
        # IsAuthenticatedOrReadOnly 사용!

    def get(self, request, format=None):
        blog_list = Blog.objects.all().order_by('-created_at').select_related('author')
        # ViewSet에서는 페이지네이션 자동으로 해주는데, 여기선 직접 설정해줘야 함
        paginator = PageNumberPagination()
        queryset = paginator.paginate_queryset(blog_list, request)

        serializer = BlogSerializer(queryset, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            blog = serializer.save(author=request.user)
            # serializer에는 commit=False를 사용할 수 없음

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogDetailAPIView(APIView):
    object = None
    permission_classes = [IsAuthorOrReadOnly]
    def get(self, request, format=None, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        serializer = BlogSerializer(blog, many=False)   # 여러개일 때는 many True, 한개일 때는 False
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        serializer = BlogSerializer(blog, data=request.data, partial=True)  # partial=True : 일부만 가져와도 Ok
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        blog = self.get_object(request, *args, **kwargs)
        blog.delete()

        return Response({
            'deleted': True,
            'pk' : kwargs.get('pk',0)
        }, status=status.HTTP_200_OK)

    def get_object(self, request, *args, **kwargs):
        # 중복 요청 방지
        if self.object :
            return self.object

        blog_list = Blog.objects.all().select_related('author')
        pk = kwargs.get('pk', 0)

        # blog = blog_list.filter(pk=pk).first()
        # if not blog :
        #     raise Http404
        blog = get_object_or_404(blog_list, pk=pk)  # 첫번째 인자로 쿼리셋 혹은 모델 둘 다 올 수 있음
        self.object = blog
        return blog


@api_view(['GET'])
@schema(AutoSchema())
def detail_view(request, pk) :
    blog_list = Blog.objects.all().select_related('author')

    blog = get_object_or_404(blog_list, pk=pk)

    serializer = BlogSerializer(blog, many=False)
    return Response(serializer.data)