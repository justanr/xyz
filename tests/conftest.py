from unittest import mock
from datetime import datetime
import pytest


@pytest.fixture
def clock():
    clock = mock.create_autospec(datetime)
    clock.now.return_value = datetime(2015, 10, 11)
    return clock
