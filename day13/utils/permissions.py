from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS :
            return True

        try :
            obj = view.get_object(request, *view.args, **view.kwargs)
        except TypeError :
            obj = view.get_object()
            # generics에서는 인자를 넣어주지 않음
        return obj.author == request.user