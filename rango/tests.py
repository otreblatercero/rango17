# -*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from rango.models import Category, Page
import datetime
from django.utils import timezone

def add_cat(name, views, likes):
	c = Category.objects.get_or_create(name=name)[0]
	c.views = views
	c.likes = likes
	c.save()
	return c

def create_page():
	now = timezone.now()
	cat = add_cat('test_cat', 1, 1)
	page = Page.objects.get_or_create(category=cat)[0]
	page.title = 'test'
	page.url = 'http://www.test.com'
	page.views = 1

	return page

class IndexViewTests(TestCase):
	def test_index_view_with_no_categories(self):
		"""
		If no questions exists, an appropriate message should be displayed.
		"""
		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "There are no categories present.")
		self.assertQuerysetEqual(response.context['categories'], [])

	def test_index_view_with_categories(self):
		"""
		If no questions exist, an appropriate message should be displayed.
		"""

		add_cat('test', 1, 1)
		add_cat('temp', 1, 1)
		add_cat('tmp', 1, 1)
		add_cat('tmp test temp', 1, 1)

		response = self.client.get(reverse('index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "tmp test temp")

		num_cats = len(response.context['categories'])
		self.assertEqual(num_cats, 4)

class CategoryMethodTests(TestCase):

	def test_ensure_views_are_positive(self):
		"""
			ensure_views_are_positive should results True for categories where views are zero or positive
		"""
		cat = Category(name='test', views=-5, likes=0)
		cat.save()
		self.assertEqual((cat.views >= 0), True)

	def test_slug_line_creation(self):
		"""
		slug_line_creation checks to make sure that when we add a category an appropriate slug line is created
		i.e. "Random Category String" -> "random-category-string"
		"""
		cat = Category(name=u'Random Category String')
		cat.save()

		self.assertEqual(cat.slug, u'random-category-string')

class PageMethodTests(TestCase):

	def test_last_visit_not_in_future(self):
		now = timezone.now()
		page = create_page()
		page.first_visit = now
		page.last_visit =now + datetime.timedelta(days=1)

		self.assertEqual(page.last_visit_is_after_first(), True )

	def test_visits_from_future(self):
		now = timezone.now()
		page = create_page()
		page.first_visit = now - datetime.timedelta(days=1)
		page.last_visit = now - datetime.timedelta(days=1)
		print
		print "first", page.first_visit
		print "last ", page.last_visit
		print "now  ", now

		self.assertEqual(page.visits_not_in_future(), True)
