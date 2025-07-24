from django.shortcuts import render, get_object_or_404

from todo.models import Todo

def todo_list(request):
    todos = Todo.objects.all()
    context = {'todos' : todos}

    return render(request, template_name='todo_list.html', context=context)

def todo_info(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    context = {'todo' : todo}
    return render(request, template_name='todo_info.html', context=context)