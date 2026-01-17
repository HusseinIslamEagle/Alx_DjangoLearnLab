from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile


def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'


def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'


def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'


@user_passes_test(is_admin)
def admin_view(request):
    return HttpResponse("Admin content")


@user_passes_test(is_librarian)
def librarian_view(request):
    return HttpResponse("Librarian content")


@user_passes_test(is_member)
def member_view(request):
    return HttpResponse("Member content")
