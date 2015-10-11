from xyz.entities.post import Post
from xyz.handlers.post import PostMaker, PostEditor
from xyz.repositories import PostRepositoryABC

from datetime import datetime
from unittest import mock
import pytest


@pytest.fixture
def maker(request, clock):
    request.cls.clock = clock


@pytest.mark.usefixtures('maker')
class TestPostMaker:
    def setup(self):
        self.posts = mock.create_autospec(PostRepositoryABC)
        self.maker = PostMaker(posts=self.posts, clock=self.clock)

    def test_create_new_draft_post_persists(self):
        self.maker.create_draft(title='Fhtagn Daaz', author=object(),
                                text='Introducing Grape Old Ones')

        assert self.posts.persist.call_count == 1

    def test_create_published_post_persists(self, clock):
        self.maker.create_published(title='Fhtagn Daaz', author=object(),
                                    text='Introducing Grape Old Ones')

        self.posts.persist.call_count == 1

    def test_create_scheduled_post_persists(self, clock):
        self.maker.schedule_post(title='Fhtagn Daaz', author=object(),
                                 text='Introducing Grape Old Ones',
                                 when=datetime(2015, 10, 12))

        assert self.posts.persist.call_count == 1


class TestPostEditor:
    def setup(self):
        self.dummy_post = Post(object(), 'Fhtagn Daaz', 'Grape Old Ones',
                               created_at=datetime(2015, 10, 11), id=1)
        self.posts = mock.create_autospec(PostRepositoryABC)
        self.posts.find_by_id.return_value = self.dummy_post
        self.editor = PostEditor(posts=self.posts)

    def test_add_category_to_post(self):
        self.editor.add_category(post_id=1, category='Primal Ice Screams')

        assert self.dummy_post.categories == {'Primal Ice Screams'}

    def test_remove_category_from_post(self):
        self.dummy_post.categories = {'Primal Ice Screams'}
        self.editor.remove_category(post_id=1, category='Primal Ice Screams')

        assert self.dummy_post.categories == set()

    def test_edit_post_title(self):
        self.editor.edit(post_id=1, title='Cthocolate')

        assert self.dummy_post.title == 'Cthocolate'

    def test_edit_post_text(self):
        self.editor.edit(post_id=1, text='Grape is gross')

        assert self.dummy_post.text == 'Grape is gross'
