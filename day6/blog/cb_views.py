from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.urls.base import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.models import Blog, Comment
from blog.forms import CommentForm


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


class BlogDetailView(ListView) :
    model = Comment
    # queryset = Blog.objects.all().prefetch_related('comment_set', 'comment_set__author')
    template_name = 'blog_detail.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Blog, pk=kwargs['blog_pk'])
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(blog=self.object).prefetch_related('author')

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #
    #     return queryset.filter(id__lte=40)
    #
    # def get_object(self):
    #     object = super().get_object()
    #
    #     return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['blog'] = self.object
        return context

    # def post(self, *args, **kwargs):
    #     comment_form = CommentForm(self.request.POST)
    #
    #     if not comment_form.is_valid():
    #         self.object = self.get_object()
    #         context = self.get_context_data(object=self.object)
    #         context['comment_form'] = comment_form
    #         return self.render_to_response(context)
    #
    #     if not self.request.user.is_authenticated:
    #         raise Http404
    #
    #     comment = comment_form.save(commit=False)
    #     comment.blog_id = self.kwargs['pk']
    #     comment.author = self.request.user
    #     comment.save()
    #
    #     return HttpResponseRedirect(reverse_lazy('blog:detail', kwargs={'pk': self.kwargs['pk']}))


class BlogCreateView(LoginRequiredMixin, CreateView) :
    model = Blog
    template_name = 'blog_form.html'
    fields = ['category', 'title', 'content']

    def form_valid(self, form) :
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self) :
    #     return reverse_lazy('cb_blog:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['sub_title'] = "작성"
        context['btn_name'] = "생성"
        return context


class BlogUpdateView(LoginRequiredMixin, UpdateView) :
    model = Blog
    template_name = 'blog_form.html'
    fields = ['category', 'title', 'content']

    def get_queryset(self) :
        queryset = super().get_queryset()
        if self.request.user.is_staff :
            return queryset
        return queryset.filter(author=self.request.user)

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['sub_title'] = "수정"
        context['btn_name'] = "수정"
        return context

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


class CommentCreateView(LoginRequiredMixin, CreateView) :
    model = Comment
    form_class = CommentForm

    def get(self, *args, **kwargs) :
        raise Http404



    def form_valid(self, form) :
        blog = self.get_blog()
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.blog = blog
        self.object.save()
        return HttpResponseRedirect(reverse('blog:detail', kwargs={'blog_pk': blog.pk}))


    def get_blog(self):
        pk = self.kwargs['blog_pk']
        blog = get_object_or_404(Blog, pk=pk)
        return blog
