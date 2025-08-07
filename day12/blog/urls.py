from django.urls.conf import path, include
from blog.views import api_views
from rest_framework import routers

app_name = 'api'

router = routers.DefaultRouter(trailing_slash=False)
router.register(f'users', api_views.UserViewSet, basename='user')
router.register(r'blogs', api_views.BlogViewSet, basename='blog')

urlpatterns = [
    # path('', api_views.blog_list, name='blog_list'),
    path('', include(router.urls))
]