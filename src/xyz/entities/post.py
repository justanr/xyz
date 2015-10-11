"""
    xyz.entities.post
    ~~~~~~~~~~~~~~~~~
    Copyright 2015 Alec Nikolas Reiter
    Licensed under MIT, see LICENSE for more details
"""
from datetime import datetime
from enum import Enum
from ..exceptions import PostError


class PostStatus(Enum):
    draft = 0
    scheduled = 1
    published = 2


class Post(object):
    def __init__(self, author, title, text, created_at, id=None,
                 categories=None, status=PostStatus.draft, published_at=None):
        self.id = id
        self.author = author
        self.title = title
        self.text = text
        self.status = status
        self.categories = categories or set()
        self.created_at = created_at
        self.published_at = published_at

    def add_category(self, category):
        self.categories.add(category)

    def remove_category(self, category):
        try:
            self.categories.remove(category)
        except KeyError:
            raise PostError('Category {0} not found on post'.format(category)) from None

    def publish(self, clock=datetime):
        self.status = PostStatus.published
        self.published_at = clock.now()

    def revert_to_draft(self):
        if self.status == PostStatus.draft:
            raise PostError("Can't revert unpublished post to draft")

        self.status = PostStatus.draft
        self.published_at = None

    def schedule(self, when, clock=datetime):
        if clock.now() > when:
            raise PostError("Can't retroactively schedule post")

        self.status = PostStatus.scheduled
        self.published_at = when

    def edit_title(self, title):
        self.title = title

    def edit_text(self, text):
        self.text = text
