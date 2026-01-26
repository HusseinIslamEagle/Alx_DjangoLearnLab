from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from .forms import ExampleForm


def book_list(request):
    form = ExampleForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('title')
        if query:
            books = Book.objects.filter(title__icontains=query)

    return render(request, 'bookshelf/book_list.html', {
        'form': form,
        'books': books
    })


def secure_view(request):
    response = HttpResponse("Secure Content")
    response['Content-Security-Policy'] = "default-src 'self'"
    return response
