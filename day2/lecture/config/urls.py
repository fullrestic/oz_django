"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http.response import Http404
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import render, redirect
from bookmark import views


def book_list(request) :
    # book_text = ''
    #
    # for i in range(0, 10) :
    #     book_text += f'book {i}<br>'
    #
    # return HttpResponse(book_text)

    return render(request, template_name='book_list.html', context={'range': range(0, 10)})

def book(request, num) :
    # book_text = f'book {num}번 페이지입니다.'
    # return HttpResponse(book_text)

    return render(request, template_name='book_detail.html', context={'num': num})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('bookmark/', views.bookmark_list),
    path('bookmark/<int:pk>/', views.bookmark_detail),
]
