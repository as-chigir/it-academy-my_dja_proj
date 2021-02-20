from django.test import TestCase, Client
from dacha import models
from unittest import mock

# Create your tests here.

import ddt
from . import constants


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

    def test_send_mail(self):
        material = models.Material(slug='slug', author=self.user,
                                   body='body')
        material.save()

        with mock.patch('dacha.views.send_mail') as mail_mock:
            self.client.post(
                '/' + str(material.id) + '/share/',
                {'name': 'name',
                 'to_email': 'e@e.com',
                 'comment': 'comment'},
            )

        mail_mock.assert_called_once()

    @mock.patch('dacha.views.send_mail')
    def test_send_mail_args(self, mail_mock):
        material = models.Material(slug='slug', author=self.user,
                                   body='body')
        material.save()

        self.client.post(
            '/' + str(material.id) + '/share/',
            {'name': 'name',
             'to_email': 'e@e.com',
             'comment': 'comment'},
            )

        body = constants.SHARE_EMAIL_BODY
        uri = "http://testserver/{y}/{m}/{d}/{slug}/".format(
            y=material.publish.year,
            m=material.publish.month,
            d=material.publish.day,
            slug=material.slug
        )
        body = body.format(title='', uri=uri, comment='comment')
        mail_mock.assert_called_with(
            'Dear name. Please take a look at next material ""',
            body,
            'admin@my.com',
            ['e@e.com']
        )

    def test_message(self):
        self.assertEqual(
            constants.SHARE_EMAIL_BODY,
            ('{title} at {uri} \n\nAdmin asks you to take a look at this'
             ' material with next comment:\n\nComment: {comment}'),
        )
