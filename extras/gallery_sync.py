#!/usr/bin/env python

"""Script to upload pictures to the gallery.

This script scans a local picture folder to determine which patients
have not yet been created in the gallery. It then creates the missing
patients.
"""

from getpass import getpass
import os

import requests


API_URL = 'http://localhost:8000/gallery/api/patients/'

API_USER = 'chathan'
API_PASSWORD = getpass('API Password: ')

LOCAL_FOLDER = input('Local folder to sync from: ')

PICTURE_EXTENSIONS = ('jpg', 'jpeg', 'png')


def crawl_pictures(start_folder):
    for root, dirs, files in os.walk(LOCAL_FOLDER):
        print("\nScanning '{0}'".format(root))

        for file in files:
            name, ext = os.path.splitext(file)

            if ext.strip('.').lower() in PICTURE_EXTENSIONS:
                print("\tFound picture '{0}'".format(name, ext))


def get_patient_list():
    """Get a list of patients from the gallery api"""
    response = requests.get(API_URL, auth=(API_USER, API_PASSWORD))
    response.raise_for_status()

    return response.json()


if __name__ == '__main__':
    crawl_pictures(LOCAL_FOLDER)
