from test_plus.test import TestCase

from blogs.models import Tag, Type, Blog
from users.models import Author


class BaseTest(TestCase):
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


class TestTag(BaseTest):

    def test__str__(self):
        self.assertEquals(self.tag_one.__str__(), 'django')

    def test_names(self):
        self.assertEquals(set(Tag.objects.names()), {'django', 'leetcode'})


class TestType(BaseTest):
    def test__str__(self):
        self.assertEquals(self.type_one.__str__(), 'python')


class TestBlog(BaseTest):
    def test__str__(self):
        self.assertEquals(self.blog_one.__str__(), '第一篇发布的文章')

    def test_get_publish(self):
        self.assertTrue(zip(Blog.objects.get_publish(), [self.blog_two, self.blog_one]))
        self.assertEquals(list(Blog.objects.get_publish(tag=self.tag_one)), [self.blog_one])
        self.assertQuerysetEqual(list(Blog.objects.get_publish(tag=self.tag_two)),
                                 map(repr, [self.blog_two, self.blog_one]))

    def test_get_tags_cloud(self):
        self.assertTrue(zip(Blog.objects.get_tags_cloud(), [('django', 1), ('leetcode', 2)]))

    def test_save(self):
        self.assertEquals(self.blog_one.slug, 'di-yi-pian-fa-bu-de-wen-zhang')
