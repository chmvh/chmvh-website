#!/usr/bin/env python

"""Script to upload pictures to the gallery.

This script scans a local picture folder to determine which patients
have not yet been created in the gallery. It then creates the missing
patients.
"""

from getpass import getpass

import requests


API_URL = 'http://localhost:8000/gallery/api/patients/'

API_USER = 'chathan'
API_PASSWORD = getpass('API Password: ')


def get_patient_list():
    """Get a list of patients from the gallery api"""
    response = requests.get(API_URL, auth=(API_USER, API_PASSWORD))
    response.raise_for_status()

    return response.json()


if __name__ == '__main__':
    print(get_patient_list())
