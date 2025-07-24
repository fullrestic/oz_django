from django.http.response import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from bookmark.models import Bookmark

def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(id__gte=50)
    context = {'bookmarks': bookmarks}
    return render(request, template_name='bookmark_list.html', context=context)

def bookmark_detail(request, pk):
    # try :
    #     bookmark = Bookmark.objects.get(pk=pk)  # get은 무조건 하나를 가져와야 함 -> 값이 없을시 오류 발생
    # except :
    #     raise Http404

    bookmark = get_object_or_404(Bookmark, pk=pk)
    context = {'bookmark': bookmark}
    return render(request, template_name='bookmark_detail.html',context=context)