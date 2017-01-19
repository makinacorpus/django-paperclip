from django.contrib.auth.models import User, Permission
from django.test import TestCase
from paperclip.models import FileType, Attachment
from .models import TestObject


class ViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user("foo_user", password="foo_password", last_name="foo lastname",
                                            first_name="foo firstname")
        object = TestObject.objects.create(name="foo object")
        cls.filetype = FileType.objects.create(type="foo filetype")
        Attachment.objects.create(content_object=object, filetype=cls.filetype, attachment_file="foo_file.txt",
                                  creator=cls.user, author="foo author", title="foo title", legend="foo legend",
                                  starred=True)
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
        self.assertRedirects(response, "/foo-url/",  fetch_redirect_response=False)
        self.assertQuerysetEqual(Attachment.objects.all(),
                                 ('<Attachment: foo_user attached >', '<Attachment: foo_user attached foo_file.txt>'))
