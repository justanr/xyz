from . import events
from enum import Enum


class ArticleStatus(Enum):
    SCHEDULED = 1
    DRAFT = 2
    PUBLISHED = 3


class Article:
    """
    Core article entity. Contains all the logic needed for creating, publishing and scheduling
    an article that does not involve actual IO. There are public members, for reading
    but they aren't meant to be written to. Instead, any changes to the state of an article
    should move through it's public methods. Changing the state of an article via setting the
    changes directly will not emit events and could cause incorrect events to be emitted in
    the future. You have been warned.
    """
    def __init__(
        self, title, content, author, written_at,
        status=None, published_at=None, id=None
    ):
        self.title = title
        self.content = content
        self.author = author
        self.written_at = written_at
        self.status = status
        self.published_at = published_at
        # persistence allowance
        self.id = id

    def draft(self):
        """
        Marks an article as a draft and emits an ArticleDrafted event::
            new_article = Article(
                'XYZ is awesome!', 'Let me tell you why XYZ is great'
                datetime.now(UTC), me
            )
            new_article.draft()

        This method can also be used to transition a published or scheduled article back to
        drafted status::

            a = article_repository.find(1)
            a.draft()
            article_repository.update(a)

        When an article is transitioned to draft status, any published information is erased.
        #TODO(justanr): Is this desired behavior?
        """
        self.status = ArticleStatus.DRAFT
        self.published_at = None
        return events.ArticleDrafted(self.id)

    def publish(self, when):
        """
        Marks an article as published at the specified time and emits an ArticlePublished event::
            new_article = Article(
                'Barrel Files Considered Harmful', 'Gonna tell you why...'
                datetime(2016, 12, 22, 15, 33, tzinfo=UTC), me
            )
            new_article.publish(datetime(2016, 12, 24, 14, 2, tzinfo=UTC)

        This method should also be used to transition existing articles to published status.
        When this method is called the published_at attribute is set to the specified datetime.
        """
        self.status = ArticleStatus.PUBLISHED
        self.published_at = when
        return events.ArticlePublished(self.id, when)

    def schedule(self, when):
        """
        Marks an article as scheduled and emits an ArticleScheduled event. Unlike draft and
        published, scheduled needs a datetime to as well, the published_at attribute is set to this
        value::
            future_article = Article(
                'Why I was wrong about barrel files', 'So,...',
                datetime(2016, 12, 23, 18, 39, tzinfo=UTC), me
            )
            future_article.schedule(datetime(2016, 12, 31, 16, 45, tzinfo=UTC)

        This method should also be used to transition existing articles to scheduled status.
        """
        self.status = ArticleStatus.SCHEDULED
        self.published_at = when
        return events.ArticleScheduled(self.id, when)

    def edit(self, content):
        """
        Changes an article's text and emits an ArticleEdited event
        """
        self.content = content
        return events.ArticleEdited(self.id)

    def rename(self, title):
        """
        Changes an article's title and emits an ArticleRenamed event that includes the
        old title and the new title
        """
        old_title = self.title
        self.title = title
        return events.ArticleRenamed(self.id, title, old_title)
