from django.db.utils import IntegrityError

import pytest

from configuration.models import PracticeInfo


class TestPracticeInfoModel(object):
    """Test cases for the PracticeInfo model"""

    @pytest.mark.django_db
    def test_create_multiple(self):
        """Test creating multiple instances.

        Since the model is a singleton, multiple instances should not
        be able to be created.
        """
        PracticeInfo.objects.create()

        with pytest.raises(IntegrityError):
            PracticeInfo.objects.create()

    @pytest.mark.django_db
    def test_defaults(self):
        """Test the defaults for a new instance.

        All fields should have defaults since an empty instance should
        be creatable.
        """
        info = PracticeInfo.objects.create()

        assert not info.accepting_clients
        assert info.accepting_clients_text == ""
        assert info.address == ""
        assert info.email == ""
        assert info.fax == ""
        assert info.not_accepting_clients_text == ""
        assert info.phone == ""

    @pytest.mark.django_db
    def test_empty(self):
        """Test creating an empty instance.

        The model should be creatable without any additional
        parameters.
        """
        PracticeInfo.objects.create()

    def test_string_conversion(self):
        """Test converting a practice info instance to a string.

        Converting an instance to a string should return the model's
        verbose name.
        """
        info = PracticeInfo()
        expected = info._meta.verbose_name.title()

        assert str(info) == expected
