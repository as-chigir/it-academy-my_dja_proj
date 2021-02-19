from django.test import TestCase, Client
from dacha import models
# Create your tests here.

import ddt


@ddt.ddt
class MaterialTestCase(TestCase):

    def setUp(self):
        super(MaterialTestCase, self).setUp()
        self.client = Client()
        self.user = models.User()
        self.user.save()

    def test_material_create_returns_200(self):
        response = self.client.post(
            '/create/',
            {'title': 'title', 'body': 'title', 'material_type': 'practice'},
        )
        self.assertEqual(response.status_code, 200)

    def test_create_one_material(self):
        self.client.post(
            '/create/',
            {'title': 'title', 'body': 'title', 'material_type': 'practice'},
        )
        models.Material.objects.get()

    def test_slug_created(self):
        self.client.post(
            '/create/',
            {'title': 'title', 'body': 'title', 'material_type': 'practice'},
        )
        obj = models.Material.objects.get()
        self.assertEqual(obj.slug, 'title')

    @ddt.data(
        ('title', 'title'),
        ('t itl e', 't-itl-e'),
        ('title  ', 'title'),
        ('tit     le', 'tit-----le'),
    )
    @ddt.unpack
    def test_slug_created_correctly(self, title, expected_slug):
        self.client.post(
            '/create/',
            {'title': title,
             'body': 'title',
             'material_type': 'practice'},
        )
        obj = models.Material.objects.get()
        self.assertEqual(obj.slug, expected_slug)
