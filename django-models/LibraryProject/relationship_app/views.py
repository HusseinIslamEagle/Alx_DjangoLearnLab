from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.views.generic.detail import DetailView

from .models import UserProfile, Book, Library


# --------------------
# Home
# --------------------
def home(request):
    return HttpResponse("Welcome to the Django App")


# --------------------
# Authentication
# --------------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})


# --------------------
# Books list (Function-based view)
# --------------------
def list_books(request):
    books = Book.objects.all()
    return render(
        request,
        'relationship_app/list_books.html',
        {'books': books}
    )


# --------------------
# Library detail (Class-based view)
# --------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# --------------------
# Role checks
# --------------------
def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'


def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'


def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


# --------------------
# Role-based views
# --------------------
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


# --------------------
# Permission-based views (Books)
# --------------------
@permission_required('relationship_app.can_add_book')
def add_book(request):
    return HttpResponse("Add Book View - Permission Granted")


@permission_required('relationship_app.can_change_book')
def edit_book(request, book_id):
    return HttpResponse(f"Edit Book {book_id} - Permission Granted")


@permission_required('relationship_app.can_delete_book')
def delete_book(request, book_id):
    return HttpResponse(f"Delete Book {book_id} - Permission Granted")
