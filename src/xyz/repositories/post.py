"""
    xyz.repositories.post
    ~~~~~~~~~~~~~~~~~~~~~
    Copyright 2015 Alec Nikolas Reiter
    Licensed under MIT, see LICENSE for details
"""


from abc import abstractmethod, ABC


class PostRepositoryABC(ABC):
    @abstractmethod
    def persist(self, post):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass
