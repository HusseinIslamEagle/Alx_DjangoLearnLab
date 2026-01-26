from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required


@permission_required('bookshelf.can_view', raise_exception=True)
def view_article(request):
    return HttpResponse("You can view articles")


@permission_required('bookshelf.can_create', raise_exception=True)
def create_article(request):
    return HttpResponse("You can create articles")


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_article(request):
    return HttpResponse("You can edit articles")


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_article(request):
    return HttpResponse("You can delete articles")
