from django.urls import (reverse)

from django.test import TestCase

from books.models import Book


class BooksTesTcase(TestCase):
    def test_no_books(self):
        response = self.client.get(reverse("books:list"))

        self.assertContains(response, 'No books found.')


    def test_book_list(self):
        Book.objects.create(title="test book1",description="test description1", isbn=1122233)
        Book.objects.create(title="test book2",description="test description2", isbn=1822234)
        Book.objects.create(title="test book3",description="test description3", isbn=6122235)

        response = self.client.get(reverse('books:list'))
        books = Book.objects.all()

        for book in books:
            self.assertContains(response, book.title)

    def test_book_detail(self):
        book = Book.objects.create(title="test book1", description="test description1", isbn=1122233)
        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))

        self.assertContains(response, book.title)
        self.assertContains(response, book.description)

