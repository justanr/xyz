from xyz.entities.post import Post, PostStatus
from xyz.exceptions import PostError
from datetime import datetime
import pytest


class TestPost:
    def setup(self):
        self.post = Post(title='Introducing Grape Old Ones',
                         text='Yummy grape flavor', created_at=datetime(2015, 10, 11),
                         author=None, categories=None)

    def test_add_category_to_post(self):
        self.post.add_category('Fhtagn Daaz')

        assert self.post.categories == {'Fhtagn Daaz'}

    def test_remove_category_from_post(self):
        self.post.add_category('Fred')

        self.post.remove_category('Fred')

        assert self.post.categories == set()

    def test_remove_nonexistent_category_causes_PostError(self):
        with pytest.raises(PostError):
            self.post.remove_category('Fhtagn Daaz')

    def test_publish_post(self, clock):
        self.post.publish(clock=clock)

        assert self.post.status == PostStatus.published
        assert self.post.published_at == datetime(2015, 10, 11)

    def test_revert_post_to_draft(self):
        self.post.publish()

        self.post.revert_to_draft()

        assert self.post.status == PostStatus.draft
        assert not self.post.published_at

    def test_cant_revert_draft_post(self):
        with pytest.raises(PostError):
            self.post.revert_to_draft()

    def test_schedule_post(self, clock):
        self.post.schedule(when=datetime(2015, 10, 12), clock=clock)

        assert self.post.status == PostStatus.scheduled
        assert self.post.published_at == datetime(2015, 10, 12)

    def test_cant_retroactively_schedule_post(self, clock):
        with pytest.raises(PostError):
            self.post.schedule(when=datetime(2015, 10, 10), clock=clock)
