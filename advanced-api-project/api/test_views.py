from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from api.models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints.
    Covers CRUD operations, permissions,
    filtering, searching, and ordering.
    """

    def setUp(self):
        # Create user for authentication tests
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.token = Token.objects.create(user=self.user)

        # Create sample author
        self.author = Author.objects.create(name='George Orwell')

        # Create sample books
        self.book1 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title='Animal Farm',
            publication_year=1945,
            author=self.author
        )

        # API endpoints
        self.list_url = '/api/books/'
        self.create_url = '/api/books/create/'
        self.detail_url = f'/api/books/{self.book1.id}/'
        self.update_url = f'/api/books/update/{self.book1.id}/'
        self.delete_url = f'/api/books/delete/{self.book1.id}/'

    # -----------------------------
    # READ TESTS (No Auth Required)
    # -----------------------------
    def test_list_books(self):
        """Anyone can list books"""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        """Anyone can retrieve a book"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], '1984')

    # -----------------------------
    # CREATE TESTS
    # -----------------------------
    def test_create_book_unauthenticated(self):
        """Unauthenticated users cannot create books"""
        data = {
            'title': 'New Book',
            'publication_year': 2020,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """Authenticated users can create books"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )
        data = {
            'title': 'Homage to Catalonia',
            'publication_year': 1938,
            'author': self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # -----------------------------
    # UPDATE TESTS
    # -----------------------------
    def test_update_book(self):
        """Authenticated users can update books"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )
        data = {
            'title': 'Nineteen Eighty-Four',
            'publication_year': 1949,
            'author': self.author.id
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Nineteen Eighty-Four')

    # -----------------------------
    # DELETE TESTS
    # -----------------------------
    def test_delete_book(self):
        """Authenticated users can delete books"""
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # -----------------------------
    # FILTER / SEARCH / ORDER TESTS
    # -----------------------------
    def test_filter_books_by_year(self):
        """Filter books by publication year"""
        response = self.client.get(
            self.list_url + '?publication_year=1949'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        """Search books by title"""
        response = self.client.get(
            self.list_url + '?search=Animal'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_books_by_year_desc(self):
        """Order books by publication year descending"""
        response = self.client.get(
            self.list_url + '?ordering=-publication_year'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data[0]['publication_year'],
            1949
        )
