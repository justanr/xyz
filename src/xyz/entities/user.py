"""
    xyz.entities.user
    ~~~~~~~~~~~~~~~~
    Copyright 2015 Alec Nikolas Reiter
    Licensed under MIT, see LICENSE for details
"""


class User:
    def __init__(self, name, email, password, registered_at, id=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.registered_at = registered_at

    @classmethod
    def register(cls, name, email, password, registered_at):
        return cls(name, email, password, registered_at=registered_at)
