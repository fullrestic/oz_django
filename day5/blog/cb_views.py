from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.urls.base import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog


class BlogListView(ListView) :
    model = Blog
    # queryset = Blog.objects.all().order_by('-created_at')
    template_name = 'blog_list.html'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')

        if q:
            from django.db.models.query_utils import Q
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        return queryset


class BlogDetailView(DetailView) :
    model = Blog
    template_name = 'blog_detail.html'

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #
    #     return queryset.filter(id__lte=40)
    #
    # def get_object(self):
    #     object = super().get_object()
    #
    #     return object

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['test'] = 'CBV'
    #     return context


class BlogCreateView(LoginRequiredMixin, CreateView) :
    model = Blog
    template_name = 'blog_create.html'
    fields = ['category', 'title', 'content']

    def form_valid(self, form) :
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self) :
    #     return reverse_lazy('cb_blog:detail', kwargs={'pk': self.object.pk})


class BlogUpdateView(LoginRequiredMixin, UpdateView) :
    model = Blog
    template_name = 'blog_update.html'
    fields = ['category', 'title', 'content']

    def get_queryset(self) :
        queryset = super().get_queryset()
        if self.request.user.is_staff :
            return queryset
        return queryset.filter(author=self.request.user)

   # def get_object(self, queryset=None) :
   #     self.object = super().get_object(queryset)
   #
   #     if self.object.author != self.request.user :
   #         raise Http404
   #     return self.object

    # def get_success_url(self) :
    #     return reverse_lazy('cb_blog:detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(LoginRequiredMixin, DeleteView) :
    model = Blog

    def get_queryset(self) :
        queryset = super().get_queryset()

        if not self.request.user.is_staff :
            return queryset.filter(author=self.request.user)
        return queryset

    def get_success_url(self) :
        return reverse_lazy('blog:list')
