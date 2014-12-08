from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from blog.models import Article

def create_article(name, status=1):
    return Article.objects.create(name=name, status=status, image=None)

class BlogTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_empty(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_status(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['articles']), 0)
        create_article('test1')
        create_article('test2', status=0)
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['articles']), 1)

    def test_order(self):
        first = create_article('test1')
        second = create_article('test2')
        response = self.client.get(reverse('home'))
        self.assertEqual(len(response.context['articles']), 2)
        self.assertEqual(str(response.context['articles']), str([first, second]))
