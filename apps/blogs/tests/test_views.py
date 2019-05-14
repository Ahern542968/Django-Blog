import json

from django.test import RequestFactory

from test_plus.test import CBVTestCase

from users.models import Author
from blogs.models import Tag, Type, Blog
from blogs.views import BlogDetailView, BlogListView

class BaseTest(CBVTestCase):
    def setUp(self):
        self.user = self.make_user('user01')
        self.author = Author.objects.create(
            author=self.user
        )
        self.tag_one = Tag.objects.create(
            name='django',
            author=self.author
        )
        self.tag_two = Tag.objects.create(
            name='leetcode',
            author=self.author
        )
        self.type_one = Type.objects.create(
            name='python',
            author=self.author
        )
        self.blog_one = Blog(
            title='第一篇发布的文章',
            author=self.author,
            status='publish',
            content='第一篇发布的文章',
            btype=self.type_one
        )
        self.blog_one.save()
        self.blog_one.tags.add(self.tag_one, self.tag_two)

        self.blog_two = Blog.objects.create(
            title='第二篇发布的文章',
            author=self.author,
            status='publish',
            content='第二篇发布的文章',
            btype=self.type_one
        )
        self.blog_two.save()
        self.blog_two.tags.add(self.tag_two)

        self.blog_three = Blog.objects.create(
            title='第一篇草稿的文章',
            author=self.author,
            status='draft',
            content='第一篇草稿的文章',
            btype=self.type_one
        )
        self.blog_three.save()
        self.blog_three.tags.add(self.tag_one)

        self.request1 = RequestFactory().get('/fake-url')

        self.request2 = RequestFactory().get('/fake-url/?tag=django')


class TestBlogListView(BaseTest):

    def test_context_data(self):
        response1 = self.get(BlogListView, request=self.request1)
        self.assertEquals(response1.status_code, 200)
        self.assertQuerysetEqual(response1.context_data['blogs'], [repr(self.blog_one), repr(self.blog_two)], ordered=False)
        self.assertContext('tag', None)

        response2 = self.get(BlogListView, request=self.request2)
        self.assertEquals(response2.status_code, 200)
        self.assertQuerysetEqual(response2.context_data['blogs'], [repr(self.blog_one)],ordered=False)
        self.assertContext('tag', 'django')

        self.assertTrue(zip(response2.context_data['tags_cloud'], [('django', 1), ('leetcode', 2)]))
        self.assertContext('blog_publish_counted', 2)


class TestBlogDetailView(BaseTest):

    def test_context_data(self):
        response = self.get(BlogDetailView, request=self.request1, pk=self.blog_one.id)
        self.response_200(response)
        self.assertEqual(response.context_data['blog'], self.blog_one)

        self.assertTrue(zip(response.context_data['tags_cloud'], [('django', 1), ('leetcode', 2)]))
        self.assertContext('blog_publish_counted', 2)
