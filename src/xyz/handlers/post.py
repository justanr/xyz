"""
    xyz.handlers.post
    ~~~~~~~~~~~~~~~~~
    Copyright 2015 Alec Nikolas Reiter
    Licensed under MIT, see LICENSE for details
"""

from ..entities import Post
from datetime import datetime


class PostMaker:
    "Handles orchestrations of all actions needed to create a new post"
    def __init__(self, posts, clock=datetime):
        self._posts = posts
        self._clock = clock

    def create_draft(self, title, text, author, categories=None):
        post = self._create_post(author, title, text, categories=categories)

        self._posts.persist(post)

    def create_published(self, title, text, author, categories=None):
        post = self._create_post(author, title, text, categories=categories)
        post.publish()

        self._posts.persist(post)

    def schedule_post(self, title, text, author, when, categories=None):
        post = self._create_post(title, text, author, categories)
        post.schedule(when, self._clock)

        self._posts.persist(post)

    def _create_post(self, title, text, author, categories):
        return Post(author, title, text, categories=categories,
                    created_at=self._clock.now())


class PostEditor:
    "Handles coordination needed for editing posts"
    def __init__(self, posts):
        self._posts = posts

    def add_category(self, post_id, category):
        post = self._posts.find_by_id(post_id)

        post.add_category(category)

        self._posts.persist(post)

    def remove_category(self, post_id, category):
        post = self._posts.find_by_id(post_id)

        post.remove_category(category)

        self._posts.persist(post)

    def edit(self, post_id, title=None, text=None):
        post = self._posts.find_by_id(post_id)

        if title is not None:
            post.edit_title(title)

        if text is not None:
            post.edit_text(text)

        self._posts.persist(post)

    def schedule_post(self, post_id, when, clock=datetime):
        post = self._posts.find_by_id(post_id)
        post.schedule(when, clock)
        self._posts.persist(post)

    def revert_to_draft(self, post_id):
        post = self._posts.find_by_id(post_id)
        post.revert_to_draft()
        self._posts.persist(post)

    def publish_post(self, post_id, clock=datetime):
        post = self._posts.find_by_id(post_id)
        post.publish(clock=clock)
        self._posts.persist(post)
