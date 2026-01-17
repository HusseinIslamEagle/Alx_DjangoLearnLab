from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required


@permission_required('relationship_app.can_add_book')
def add_book(request):
    return HttpResponse("Add Book View - Permission Granted")


@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    return HttpResponse("Edit Book View - Permission Granted")


@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    return HttpResponse("Delete Book View - Permission Granted")
