from django.contrib.contenttypes.models import ContentType

from test_plus.test import TestCase

from users.models import Author
from blogs.models import Type, Blog
from likes.models import Like


class TestLike(TestCase):

    def setUp(self):
        self.user = self.make_user()

        self.author = Author.objects.create(
            author=self.user
        )

        self.type = Type.objects.create(
            name='python',
            author=self.author
        )

        self.blog = Blog.objects.create(
            title='第一篇发布的文章',
            author=self.author,
            status='publish',
            content='第一篇发布的文章',
            btype=self.type
        )

        content_type = ContentType.objects.get(model='blog')

        self.like = Like.objects.create(
            user=self.user,
            content_type=content_type,
            object_id=1,
        )

    def test__str__(self):
        self.assertEqual(self.like.__str__(), 'testuser')
