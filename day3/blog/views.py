from http.client import responses

from django.shortcuts import render, get_object_or_404

from blog.models import Blog


def blog_list(request):
    blogs = Blog.objects.all()

    visits = int(request.COOKIES.get('visit', 0)) + 1    # visit키의 값을 가져오고, 존재하지 않으면 0을 가져옴
    request.session['count'] = request.session.get('count', 0) + 1

    context = {
        'blogs': blogs,
        'count' : request.session['count']
    }

    response = render(request, 'blog_list.html', context)
    response.set_cookie('visit', visits)
    return response

def blog_detail(request, pk) :
    blog = get_object_or_404(Blog, pk=pk)
    context = {'blog': blog}
    return render(request, 'blog_detail.html', context)