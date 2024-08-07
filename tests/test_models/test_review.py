#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.review import Review
from os import getenv


class test_review(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_place_id(self):
        """ """
        new = self.value()
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            self.assertIsNone(new.place_id)
        else:
            self.assertEqual(type(new.place_id), str)

    def test_user_id(self):
        """ """
        new = self.value()
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            self.assertIsNone(new.user_id)
        else:
            self.assertEqual(type(new.user_id), str)

    def test_text(self):
        """ """
        new = self.value()
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            self.assertIsNone(new.text)
        else:
            self.assertEqual(type(new.text), str)
