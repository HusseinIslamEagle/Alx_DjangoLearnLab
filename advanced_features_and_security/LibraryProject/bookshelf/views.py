from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    return HttpResponse("Book list - permission granted")


@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    return HttpResponse("Create book - permission granted")


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request):
    return HttpResponse("Edit book - permission granted")


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request):
    return HttpResponse("Delete book - permission granted")
