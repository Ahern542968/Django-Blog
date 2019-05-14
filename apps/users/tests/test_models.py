from test_plus.test import TestCase
from users.models import Author


class BaseText(TestCase):
    def setUp(self):
        self.user = self.make_user()
        self.author = Author.objects.create(
            author=self.user
        )


class TestUser(BaseText):

    def test__str__(self):
        self.assertEquals(self.user.__str__(), 'testuser')

    def test__get_name(self):
        self.assertEquals(self.user.get_name(), 'testuser')
        self.user.nickname = 'Ahern'
        self.assertEquals(self.user.get_name(), 'Ahern')


class TestAuthor(BaseText):

    def test__str__(self):
        self.assertEquals(self.author.__str__(), 'testuser')
        self.user.nickname = 'Ahern'
        self.assertEquals(self.author.__str__(), 'Ahern')
