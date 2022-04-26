from io import BytesIO
from tempfile import TemporaryDirectory
from unittest.mock import patch

from django.contrib.auth.models import Permission, User
from django.contrib.messages import get_messages
from django.core.files.images import get_image_dimensions
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from paperclip.settings import get_attachment_model, get_filetype_model

from .models import TestObject, License


@override_settings(MEDIA_ROOT=TemporaryDirectory().name)
class ViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("foo_user", password="foo_password", last_name="foo lastname",
                                            first_name="foo firstname")
        object = TestObject.objects.create(name="foo object")
        cls.filetype = get_filetype_model().objects.create(type="foo filetype")
        cls.attachment = get_attachment_model().objects.create(content_object=object, filetype=cls.filetype,
                                                               attachment_file="foo_file.txt", creator=cls.user,
                                                               author="foo author", title="foo title",
                                                               legend="foo legend", starred=True)
        cls.pk = object.pk

    def test_detail_not_logged(self):
        response = self.client.get('/test_object/{pk}/'.format(pk=self.pk))
        self.assertContains(response, "You are not allowed to see attachments.")

    def test_detail_without_perm(self):
        self.client.login(username="foo_user", password="foo_password")
        response = self.client.get('/test_object/{pk}/'.format(pk=self.pk))
        self.assertContains(response, "You are not allowed to see attachments.")

    def test_detail_view(self):
        perm = Permission.objects.get(codename='read_attachment')
        self.user.user_permissions.add(perm)
        self.client.login(username="foo_user", password="foo_password")
        response = self.client.get('/test_object/{pk}/'.format(pk=self.pk))
        self.assertContains(response, "Attached files")
        self.assertContains(response, "foo title")
        self.assertContains(response, "foo_file.txt")
        self.assertContains(response, "foo legend")
        self.assertContains(response, "foo author")
        self.assertContains(response, "star-on.svg")

    def test_add_view(self):
        perm = Permission.objects.get(codename='add_attachment')
        self.user.user_permissions.add(perm)
        self.client.login(username="foo_user", password="foo_password")

        f = SimpleUploadedFile("file.txt", b"file_content")
        response = self.client.post('/paperclip/add-for/test_app/testobject/{pk}/'.format(pk=self.pk),
                                    {'embed': 'File', 'filetype': self.filetype.pk, 'next': '/foo-url/',
                                     'attachment_file': f})
        self.assertRedirects(response, "/foo-url/", fetch_redirect_response=False)
        self.assertQuerysetEqual(get_attachment_model().objects.all(),
                                 (f'<Attachment: foo_user attached paperclip/test_app_testobject/{self.pk}/file.txt>',
                                  '<Attachment: foo_user attached foo_file.txt>'))

    def test_update_view(self):
        perm = Permission.objects.get(codename='change_attachment')
        self.user.user_permissions.add(perm)
        self.client.login(username="foo_user", password="foo_password")
        response = self.client.post('/paperclip/update/{pk}/'.format(pk=self.attachment.pk),
                                    {'embed': 'File',
                                     'filetype': self.filetype.pk,
                                     'next': '/foo-url/',
                                     'title': 'test'})
        self.assertRedirects(response, "/foo-url/", fetch_redirect_response=False)
        self.assertQuerysetEqual(get_attachment_model().objects.all(),
                                 ('<Attachment: foo_user attached foo_file.txt>', ))
        response = self.client.get('/paperclip/update/{pk}/'.format(pk=self.attachment.pk))
        self.assertContains(response, b'Update foo_file.txt')

    def test_delete_view(self):
        object_attachment = TestObject.objects.create(name="foo object")
        attachment = get_attachment_model().objects.create(content_object=object_attachment, filetype=self.filetype,
                                                           attachment_file="attach.txt", creator=self.user,
                                                           author="bar author", title="bar title",
                                                           legend="bar legend", starred=True)
        perm = Permission.objects.get(codename='delete_attachment')
        self.user.user_permissions.add(perm)
        self.client.login(username="foo_user", password="foo_password")
        self.assertQuerysetEqual(get_attachment_model().objects.all(),
                                 ('<Attachment: foo_user attached attach.txt>',
                                  '<Attachment: foo_user attached foo_file.txt>',))
        response = self.client.post('/paperclip/delete/{pk}/'.format(pk=attachment.pk))
        self.assertRedirects(response, "/", fetch_redirect_response=False)
        self.assertQuerysetEqual(get_attachment_model().objects.all(),
                                 ('<Attachment: foo_user attached foo_file.txt>', ))

    def test_delete_view_no_permission_delete(self):
        user_other = User.objects.create_user("other_user", password="other_password", last_name="other lastname",
                                              first_name="other firstname")
        object_attachment = TestObject.objects.create(name="foo object")
        attachment = get_attachment_model().objects.create(content_object=object_attachment, filetype=self.filetype,
                                                           attachment_file="attach.txt", creator=user_other,
                                                           author="bar author", title="bar title",
                                                           legend="bar legend", starred=True)
        perm = Permission.objects.get(codename='delete_attachment')
        self.user.user_permissions.add(perm)
        self.client.login(username="foo_user", password="foo_password")
        self.assertQuerysetEqual(get_attachment_model().objects.all(),
                                 ('<Attachment: other_user attached attach.txt>',
                                  '<Attachment: foo_user attached foo_file.txt>',))
        response = self.client.post('/paperclip/delete/{pk}/'.format(pk=attachment.pk))
        self.assertRedirects(response, "/", fetch_redirect_response=False)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), 'You are not allowed to delete this attachment.')
        self.assertQuerysetEqual(get_attachment_model().objects.all(),
                                 ('<Attachment: other_user attached attach.txt>',
                                  '<Attachment: foo_user attached foo_file.txt>', ))

    def test_star_view(self):
        object_attachment = TestObject.objects.create(name="foo object")
        attachment = get_attachment_model().objects.create(content_object=object_attachment, filetype=self.filetype,
                                                           attachment_file="attach.txt", creator=self.user,
                                                           author="bar author", title="bar title",
                                                           legend="bar legend")
        perm = Permission.objects.get(codename='change_attachment')
        self.user.user_permissions.add(perm)
        self.client.login(username="foo_user", password="foo_password")
        self.assertFalse(attachment.starred)
        response = self.client.post('/paperclip/star/{pk}/'.format(pk=attachment.pk))
        self.assertEqual(response.json(), {'status': 'ok', 'starred': True})
        attachment.refresh_from_db()
        self.assertTrue(attachment.starred)
        response = self.client.get('/paperclip/star/{pk}/'.format(pk=attachment.pk), {'unstar': True})
        self.assertEqual(response.json(), {'status': 'ok', 'starred': False})
        attachment.refresh_from_db()
        self.assertFalse(attachment.starred)

    def test_get_view(self):
        perm = Permission.objects.get(codename='read_attachment')
        self.user.user_permissions.add(perm)
        self.client.login(username="foo_user", password="foo_password")
        response = self.client.get('/paperclip/get/test_app/testobject/{pk}/'.format(pk=self.pk), safe=False)
        self.assertEqual(response.json(), [{"id": 1,
                                            "title": "foo title",
                                            "legend": "foo legend",
                                            "url": "/foo_file.txt",
                                            "type": "foo filetype",
                                            "author": "foo author",
                                            "filename": "foo_file.txt",
                                            "mimetype": ["text", "plain"],
                                            "is_image": False,
                                            "starred": True}])


@override_settings(MEDIA_ROOT=TemporaryDirectory().name)
class TestResizeAttachmentsOnUpload(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("foo_user", password="foo_password", last_name="foo lastname",
                                            first_name="foo firstname")
        cls.object = TestObject.objects.create(name="foo object")
        cls.filetype = get_filetype_model().objects.create(type="foo filetype")

    def get_big_dummy_uploaded_image(self):
        file = BytesIO()
        image = Image.new('RGBA', size=(2000, 4000), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test_big.png'
        file.seek(0)
        return SimpleUploadedFile(file.name, file.read(), content_type='image/png')

    def get_small_dummy_uploaded_image(self):
        file = BytesIO()
        image = Image.new('RGB', size=(20, 40), color=(155, 0, 0))
        image.save(file, 'jpeg')
        file.name = 'small.jpg'
        file.seek(0)
        return SimpleUploadedFile(file.name, file.read(), content_type='image/png')

    @patch("paperclip.models.PAPERCLIP_RESIZE_ATTACHMENTS_ON_UPLOAD", True)
    def test_attachment_is_resized(self):
        attachment = get_attachment_model().objects.create(content_object=self.object, filetype=self.filetype,
                                                           attachment_file=self.get_big_dummy_uploaded_image(), creator=self.user, author="foo author",
                                                           title="foo title", legend="foo legend", starred=True)
        self.assertEqual((640, 1280), get_image_dimensions(attachment.attachment_file))

    def test_attachment_is_not_resized_by_default(self):
        attachment = get_attachment_model().objects.create(content_object=self.object, filetype=self.filetype,
                                                           attachment_file=self.get_big_dummy_uploaded_image(), creator=self.user, author="foo author",
                                                           title="foo title", legend="foo legend", starred=True)
        self.assertEqual((2000, 4000), get_image_dimensions(attachment.attachment_file))

    @patch("paperclip.models.PAPERCLIP_RESIZE_ATTACHMENTS_ON_UPLOAD", True)
    @patch("paperclip.models.PAPERCLIP_MAX_ATTACHMENT_WIDTH", 2100)
    @patch("paperclip.models.PAPERCLIP_MAX_ATTACHMENT_HEIGHT", 100)
    def test_attachment_is_resized_per_height(self):
        attachment = get_attachment_model().objects.create(content_object=self.object, filetype=self.filetype,
                                                           attachment_file=self.get_big_dummy_uploaded_image(), creator=self.user, author="foo author",
                                                           title="foo title", legend="foo legend", starred=True)
        attachment = get_attachment_model().objects.get(title="foo title")
        self.assertEqual((50, 100), get_image_dimensions(attachment.attachment_file))

    @patch("paperclip.models.PAPERCLIP_RESIZE_ATTACHMENTS_ON_UPLOAD", True)
    @patch("paperclip.models.PAPERCLIP_MAX_ATTACHMENT_WIDTH", 100)
    @patch("paperclip.models.PAPERCLIP_MAX_ATTACHMENT_HEIGHT", 2100)
    def test_attachment_is_resized_per_width(self):
        attachment = get_attachment_model().objects.create(content_object=self.object, filetype=self.filetype,
                                                           attachment_file=self.get_big_dummy_uploaded_image(), creator=self.user, author="foo author",
                                                           title="foo title", legend="foo legend", starred=True)
        self.assertEqual((100, 200), get_image_dimensions(attachment.attachment_file))

    @patch("paperclip.models.PAPERCLIP_RESIZE_ATTACHMENTS_ON_UPLOAD", True)
    @patch("paperclip.models.PAPERCLIP_RESIZE_ATTACHMENTS_ON_UPLOAD", True)
    @patch("paperclip.models.PAPERCLIP_MAX_ATTACHMENT_WIDTH", 100)
    @patch("paperclip.models.PAPERCLIP_MAX_ATTACHMENT_HEIGHT", 2100)
    def test_attachment_is_resized_when_updated(self):
        # Create attachment with small image
        small_image = self.get_small_dummy_uploaded_image()
        attachment = get_attachment_model().objects.create(content_object=self.object, filetype=self.filetype,
                                                           attachment_file=small_image, creator=self.user, author="foo author",
                                                           title="foo title", legend="foo legend", starred=True)
        self.assertEqual((20, 40), get_image_dimensions(attachment.attachment_file))
        # Update attachment with big image and assert picture resized
        permission = Permission.objects.get(codename="change_attachment")
        self.user.user_permissions.add(permission)
        self.client.force_login(self.user)
        big_image = self.get_big_dummy_uploaded_image()
        response = self.client.post(
            reverse(
                'update_attachment',
                kwargs={'attachment_pk': attachment.pk}),
            data={
                'attachment_file': big_image,
                'filetype': self.filetype.pk,
                'author': "newauthor",
                'next': f"/test_object/{self.object.pk}",
                'embed': 'File'
            }
        )
        self.assertEqual(response.status_code, 302)
        # Refresh object
        attachment = get_attachment_model().objects.get(pk=attachment.pk)
        self.assertEqual(attachment.author, "newauthor")
        self.assertEqual((100, 200), get_image_dimensions(attachment.attachment_file))


class LicenseModelTestCase(TestCase):
    def test_str(self):
        self.assertEqual(str(License.objects.create(label="foo")), "foo")
