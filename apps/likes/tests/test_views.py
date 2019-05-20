import json

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser

from test_plus.test import CBVTestCase

from users.models import Author
from blogs.models import Type, Blog
from likes import views


class TestLike(CBVTestCase):
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

        self.request = RequestFactory().post('/fake-url', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        # QueryDict instance is immutable, request.POST是QueryDict对象，不可变
        self.request.POST = self.request.POST.copy()

    def test_change_like(self):
        self.request.user = AnonymousUser()
        self.request.POST['object_type'] = 'blog'
        self.request.POST['object_id'] = self.blog.id
        response = views.change_like(self.request)
        assert response.status_code == 200
        assert json.loads(response.content)['status'] == 'fail'
        assert json.loads(response.content)['msg'] == '用户未登录'

        self.request.user = self.user
        self.request.POST['object_type'] = 'article'
        self.request.POST['object_id'] = self.blog.id
        response = views.change_like(self.request)
        assert response.status_code == 200
        assert json.loads(response.content)['status'] == 'fail'
        assert json.loads(response.content)['msg'] == '点赞出错'

        self.request.user = self.user
        self.request.POST['object_type'] = 'blog'
        self.request.POST['object_id'] = self.blog.id
        self.assertEquals(self.blog.get_like_num, 0)
        response = views.change_like(self.request)
        assert response.status_code == 200
        assert json.loads(response.content)['status'] == 'success'
        assert json.loads(response.content)['msg'] == '点赞成功'
        self.assertEqual(json.loads(response.content)['is_like'], True)
        assert json.loads(response.content)['like_num'] == 1

        self.request.user = self.user
        self.request.POST['object_type'] = 'blog'
        self.request.POST['object_id'] = self.blog.id
        self.assertEquals(self.blog.get_like_num, 1)
        response = views.change_like(self.request)
        assert response.status_code == 200
        assert json.loads(response.content)['status'] == 'success'
        assert json.loads(response.content)['msg'] == '取消点赞'
        self.assertEqual(json.loads(response.content)['is_like'], False)
        assert json.loads(response.content)['like_num'] == 0

