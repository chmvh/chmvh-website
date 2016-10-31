from django.test import RequestFactory

import pytest

from configuration.context_processors import practice_info
from configuration.models import PracticeInfo


class TestPracticeInfoContextProcessor(object):
    """Test cases for the practice info context processor"""

    def setup_method(self):
        """Create a request factory to use"""
        self.factory = RequestFactory()

    @pytest.mark.django_db
    def test_existing_practice(self):
        """Test the processor with an existing practice.

        If a practice already exists, it should be returned.
        """
        request = self.factory.get('/')
        info = PracticeInfo.get_solo()
        info.address = 'foo\nbar'
        info.save()

        context = practice_info(request)

        assert context == {'practice_info': info}

    @pytest.mark.django_db
    def test_no_practice(self):
        """Test the processor with no existing practice.

        If no practice exists, one should be created.
        """
        request = self.factory.get('/')
        context = practice_info(request)
        expected = {
            'practice_info': PracticeInfo.get_solo(),
        }

        assert context == expected
