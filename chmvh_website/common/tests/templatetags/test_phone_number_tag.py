from common.templatetags.common import phone_number


class TestPhoneNumberTag(object):
    """Test cases for the phone number tag"""

    def test_multi_whitespace(self):
        """Test passing in a string with lots of whitespace.

        Whitespace more than 1 character wide should be condensed down
        to one non-breaking space.
        """
        num = "(555)   555-5555"
        out = phone_number(num)

        assert out == "(555)&nbsp;555-5555"

    def test_standard_number(self):
        """Test passing in a standard 10 digit phone number.

        The output should replace whitespace with non-breaking spaces.
        """
        num = "(555) 555-5555"
        out = phone_number(num)

        assert out == "(555)&nbsp;555-5555"
