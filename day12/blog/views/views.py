from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls.base import reverse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.http.response import HttpResponseRedirect

from blog.models import Blog


class BlogListView(ListView) :
    model = Blog
    queryset = Blog.objects.all()
    template_name = 'list.html'

class BlogCreateView(LoginRequiredMixin, CreateView) :
    model = Blog
    fields = ['title', 'content', 'published_at']
    template_name = 'form.html'

    def form_valid(self, form) :
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        return HttpResponseRedirect(reverse('blog_list'))