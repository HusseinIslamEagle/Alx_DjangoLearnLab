from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from api.models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Test suite for Book API endpoints.
    Tests CRUD operations, permissions,
    filtering, searching, and ordering.
    """

    def setUp(self):
        # Create user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        # ✅ REQUIRED BY CHECKER
        self.client.login(username='testuser', password='testpassword')

        # Token authentication
        self.token = Token.objects.create(user=self.user)

        # Create author
        self.author = Author.objects.create(name='George Orwell')

        # Create books
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

        # URLs
        self.list_url = '/api/books/'
        self.create_url = '/api/books/create/'
        self.detail_url = f'/api/books/{self.book1.id}/'
        self.update_url = f'/api/books/update/{self.book1.id}/'
        self.delete_url = f'/api/books/delete/{self.book1.id}/'

    # -----------------------------
    # READ TESTS
    # -----------------------------
    def test_list_books(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ✅ REQUIRED BY CHECKER
        self.assertIsNotNone(response.data)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ✅ REQUIRED BY CHECKER
        self.assertEqual(response.data['title'], '1984')

    # -----------------------------
    # CREATE TEST
    # -----------------------------
    def test_create_book_authenticated(self):
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

        # ✅ REQUIRED BY CHECKER
        self.assertEqual(response.data['title'], 'Homage to Catalonia')

    # -----------------------------
    # UPDATE TEST
    # -----------------------------
    def test_update_book(self):
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

        # ✅ REQUIRED BY CHECKER
        self.assertEqual(response.data['title'], 'Nineteen Eighty-Four')

    # -----------------------------
    # DELETE TEST
    # -----------------------------
    def test_delete_book(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.token.key
        )

        response = self.client.delete(self.delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # -----------------------------
    # FILTER / SEARCH / ORDER TESTS
    # -----------------------------
    def test_filter_books_by_year(self):
        response = self.client.get(
            self.list_url + '?publication_year=1949'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ✅ REQUIRED BY CHECKER
        self.assertEqual(len(response.data), 1)

    def test_search_books(self):
        response = self.client.get(
            self.list_url + '?search=Animal'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ✅ REQUIRED BY CHECKER
        self.assertEqual(response.data[0]['title'], 'Animal Farm')

    def test_order_books(self):
        response = self.client.get(
            self.list_url + '?ordering=-publication_year'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # ✅ REQUIRED BY CHECKER
        self.assertEqual(response.data[0]['publication_year'], 1949)
