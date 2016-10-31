from datetime import datetime
from unittest import mock

from common.templatetags.common import copyright_years


class TestCopyrightYearsTag(object):
    """Test cases for the copyright_years template tag"""

    def test_2016(self):
        """Test the template tag in 2016.

        If the current year is 2016, then the output should just be
        2016."""
        date = datetime.strptime('2016', '%Y')
        with mock.patch(
                'common.templatetags.common.timezone.now',
                autospec=True,
                return_value=date) as mock_now:
            out = copyright_years()

        assert out == '2016'
        assert mock_now.call_count == 1

    def test_future(self):
        """Test the tag for years after 2016.

        If the year is past 2016, the tag should output a range of
        years.
        """
        date = datetime.strptime('2017', '%Y')
        with mock.patch(
                'common.templatetags.common.timezone.now',
                autospec=True,
                return_value=date) as mock_now:
            out = copyright_years()

        assert out == '2016 &ndash; 2017'
        assert mock_now.call_count == 1
