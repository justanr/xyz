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
    def __init__(self, posts):
        self._posts = posts

    def create_draft(self, title, text, author, categories=None, clock=datetime):
        post = self._create_post(author, title, text, clock=clock.now(), categories=categories)

        self._posts.persist(post)

    def create_published(self, title, text, author, categories=None, clock=datetime):
        post = self._create_post(author, title, text, clock=clock.now(), categories=categories)
        post.publish()

        self._posts.persist(post)

    def schedule_post(self, title, text, author, when, categories=None, clock=datetime):
        post = self._create_post(title, text, author, categories, clock)
        post.schedule(when, clock)

        self._posts.persist(post)

    def _create_post(self, title, text, author, categories, clock):
        return Post(author, title, text, categories=categories, created_at=clock.now())


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
