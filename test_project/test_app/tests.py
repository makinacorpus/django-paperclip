from io import BytesIO

from django.contrib.auth.models import Permission, User
from django.core.files.images import get_image_dimensions
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.test.utils import override_settings
from PIL import Image

from paperclip.settings import get_attachment_model, get_filetype_model

from .models import TestObject, Attachment


class ViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("foo_user", password="foo_password", last_name="foo lastname",
                                            first_name="foo firstname")
        object = TestObject.objects.create(name="foo object")
        cls.filetype = get_filetype_model().objects.create(type="foo filetype")
        get_attachment_model().objects.create(content_object=object, filetype=cls.filetype,
                                              attachment_file="foo_file.txt", creator=cls.user, author="foo author",
                                              title="foo title", legend="foo legend", starred=True)
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
        response = self.client.post('/paperclip/add-for/test_app/testobject/{pk}/'.format(pk=self.pk),
                                    {'embed': False, 'filetype': self.filetype.pk, 'next': '/foo-url/'})
        self.assertRedirects(response, "/foo-url/", fetch_redirect_response=False)
        self.assertQuerysetEqual(get_attachment_model().objects.all(),
                                 ('<Attachment: foo_user attached >', '<Attachment: foo_user attached foo_file.txt>'))


class TestResizeAttachmentsOnUpload(TestCase):

    def get_big_dummy_uploaded_image(self, name='dummy_img.svg'):
        file = BytesIO()
        image = Image.new('RGBA', size=(2000, 4000), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test_big.png'
        file.seek(0)
        return SimpleUploadedFile(file.name, file.read(), content_type='image/png')

    @override_settings(PAPERCLIP_RESIZE_ATTACHMENTS_ON_UPLOAD=True)
    def test_attachment_is_resized(self):
        attachment = Attachment.create(attachment_file=self.get_big_dummy_uploaded_image())
        self.assertEqual((640, 1280), get_image_dimensions(attachment.attachment_file))

    @override_settings(PAPERCLIP_RESIZE_ATTACHMENTS_ON_UPLOAD=False)
    def test_attachment_is_not_resized(self):
        attachment = Attachment.create(attachment_file=self.get_big_dummy_uploaded_image())
        self.assertEqual((2000, 4000), get_image_dimensions(attachment.attachment_file))

    @override_settings(PAPERCLIP_RESIZE_ATTACHMENTS_ON_UPLOAD=True)
    @override_settings(PAPERCLIP_MAX_ATTACHMENT_WIDTH=2100)
    @override_settings(PAPERCLIP_MAX_ATTACHMENT_HEIGHT=100)
    def test_attachment_is_resized_per_height(self):
        attachment = Attachment.create(attachment_file=self.get_big_dummy_uploaded_image())
        self.assertEqual((50, 100), get_image_dimensions(attachment.attachment_file))

    @override_settings(RESIZE_ATTACHMENTS_ON_UPLOAD=True)
    @override_settings(MAX_ATTACHMENT_WIDTH=100)
    @override_settings(MAX_ATTACHMENT_HEIGHT=2100)
    def test_attachment_is_resized_per_width(self):
        attachment = Attachment.create(attachment_file=self.get_big_dummy_uploaded_image())
        self.assertEqual((100, 200), get_image_dimensions(attachment.attachment_file))
