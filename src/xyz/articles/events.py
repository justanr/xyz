from collections import namedtuple

ArticleDrafted = namedtuple('ArticleDrafted', ['article_id'])
ArticlePublished = namedtuple('ArticlePublished', ['article_id', 'published_at'])
ArticleScheduled = namedtuple('ArticleScheduled', ['article_id', 'scheduled_for'])
ArticleEdited = namedtuple('ArticleEdited', ['article_id'])
ArticleRenamed = namedtuple('ArticleRenamed', ['article_id', 'new_title', 'old_title'])
