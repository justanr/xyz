from xyz.articles import Article, ArticleStatus, events

from pytz import UTC
import pytest

from collections import namedtuple
from datetime import datetime
from operator import methodcaller


class TestArticle:
    User = namedtuple('User', [])
    PUBLISH_DATE = datetime(2015, 1, 1, tzinfo=UTC)
    SCHEDULE_DATE = datetime(2099, 1, 1, tzinfo=UTC)

    def test_draft_article(self):
        event = self.article.draft()
        assert self.article.status == ArticleStatus.DRAFT
        assert event == events.ArticleDrafted(self.article.id)

    def test_publish_article(self):
        event = self.article.publish(self.PUBLISH_DATE)
        assert self.article.status == ArticleStatus.PUBLISHED
        assert self.article.published_at == self.PUBLISH_DATE
        assert event == events.ArticlePublished(self.article.id, self.PUBLISH_DATE)

    def test_schedule_article(self):
        event = self.article.schedule(self.SCHEDULE_DATE)
        assert self.article.status == ArticleStatus.SCHEDULED
        assert self.article.published_at == self.SCHEDULE_DATE
        assert event == events.ArticleScheduled(self.article.id, self.SCHEDULE_DATE)

    @pytest.mark.parametrize('setup', [
        methodcaller('publish', datetime.now(UTC)),
        methodcaller('schedule', datetime.now(UTC))
    ])
    def test_move_existing_to_draft(self, setup):
        setup(self.article)
        self.article.draft()
        assert self.article.published_at is None
        assert self.article.status == ArticleStatus.DRAFT

    @pytest.mark.parametrize('setup', [
        methodcaller('draft'),
        methodcaller('schedule', SCHEDULE_DATE)
    ])
    def test_move_existing_to_published(self, setup):
        setup(self.article)
        self.article.publish(self.PUBLISH_DATE)
        assert self.article.published_at == self.PUBLISH_DATE
        assert self.article.status == ArticleStatus.PUBLISHED

    @pytest.mark.parametrize('setup', [
        methodcaller('draft'),
        methodcaller('publish', PUBLISH_DATE)
    ])
    def test_move_existing_to_scheduled(self, setup):
        setup(self.article)
        self.article.schedule(self.SCHEDULE_DATE)
        assert self.article.published_at == self.SCHEDULE_DATE
        assert self.article.status == ArticleStatus.SCHEDULED

    def test_rename(self):
        event = self.article.rename('A Better Test')
        assert self.article.title == 'A Better Test'
        assert event == events.ArticleRenamed(self.article.id, 'A Better Test', 'a test')

    def test_edit(self):
        event = self.article.edit('More testaronis')
        assert self.article.content == "More testaronis"
        assert event == events.ArticleEdited(self.article.id)

    @pytest.fixture(autouse=True)
    def create_article(self):
        self.article = Article(
            title='a test',
            content='just a little testaroni',
            author=self.User(),
            written_at=datetime(2016, 12, 24, 3, 47, tzinfo=UTC)
        )
