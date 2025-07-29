from django.contrib import admin
from django.shortcuts import redirect, render
from django.urls import path, include
from django.views.generic.base import TemplateView, RedirectView, View

from blog import views, cb_views
from config.settings import LOGIN_REDIRECT_URL
from member import views as member_views

# class AboutView(TemplateView):
#     template_name = 'about.html'
#
# class TestView(View) :
#     def get(self, request):
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('blog.urls')),
    path('fb/', include('blog.fbv_urls')),

    # auth
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', member_views.sign_up, name='signup'),
    path('login/', member_views.login, name='login'),

    # # path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    # path('about/', AboutView.as_view(), name='about'),
    # path('redirect/', RedirectView.as_view(pattern_name='about'), name='redirect'),
    # # path('redirect2/', lambda req : redirect('about')),
    # path('test/', TestView.as_view(), name='test'),
]
#         return render(request, 'test_get.html')
#
#     def post(self, request):
#         return render(request, 'test_post.html')
