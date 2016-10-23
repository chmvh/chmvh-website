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


def get_patient_list():
    """Get a list of patients from the gallery api"""
    response = requests.get(API_URL, auth=(API_USER, API_PASSWORD))
    response.raise_for_status()

    patients = []

    for patient in response.json():
        name = '{0} {1}'.format(patient['first_name'], patient['last_name'])

        patients.append(name)

    return patients


def upload_picture(path, name):
    fname, lname = name.rsplit(' ', 1)
    data = {
        'first_name': fname,
        'last_name': lname,
    }

    with open(path, 'rb') as f:
        files = {
            'picture': f,
        }

        requests.post(
            API_URL,
            auth=(API_USER, API_PASSWORD),
            data=data,
            files=files)


def upload_pictures(start_folder):
    existing_patients = get_patient_list()

    for root, dirs, files in os.walk(start_folder):
        for file in files:
            name, ext = os.path.splitext(file)

            if ext.strip('.').lower() in PICTURE_EXTENSIONS:
                if name not in existing_patients:
                    path = os.path.join(root, file)

                    upload_picture(path, name)


if __name__ == '__main__':
    upload_pictures(LOCAL_FOLDER)
