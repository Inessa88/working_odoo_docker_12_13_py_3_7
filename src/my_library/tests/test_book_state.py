# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, SingleTransactionCase, SavepointCase, tagged


# TransactionCase = new setUp before and clean up after EVERY test

@tagged('-at_install', 'post_install', 'local_test')
class TestBookState(TransactionCase):

    def setUp(self, *args, **kwargs):
        super(TestBookState, self).setUp(*args, **kwargs)
        self.test_book = self.env['library.book'].create({'name': 'Book 1'})

    def test_button_available(self):
        """Make available button"""
        self.test_book.make_available()
        self.assertEqual(self.test_book.state, 'available',
                'Book state should changed to available')

    def test_button_lost(self):
        """Make lost button"""
        self.test_book.make_lost()
        self.assertEqual(self.test_book.state, 'lost',
                'Book state should changed to lost')

# # SingleTransactionCase = new setUp before EVERY test and clean up after LAST test

# @tagged('-at_install', 'post_install', 'local_test')
# class TestBookState(SingleTransactionCase):

#     def setUp(self, *args, **kwargs):
#         super(TestBookState, self).setUp(*args, **kwargs)
#         self.test_book = self.env['library.book'].create({'name': 'Book 1'})

#     def test_button_available(self):
#         """Make available button"""
#         self.test_book.make_available()
#         self.assertEqual(self.test_book.state, 'available',
#                 'Book state should changed to available')

#     def test_button_lost(self):
#         """Make lost button"""
#         self.test_book.make_lost()
#         self.assertEqual(self.test_book.state, 'lost',
#                 'Book state should changed to lost')

# # SavepointCase = new setUpClass before ONLY FIRST test

# @tagged('-at_install', 'post_install', 'local_test')
# class TestBookState(SavepointCase):
#     @classmethod
#     def setUpClass(cls):
#         super(TestBookState, cls).setUpClass()
#         cls.test_book = cls.env['library.book'].create({'name': 'Book 1'})

#     def test_button_available(self):
#         """Make available button"""
#         self.test_book.make_available()
#         self.assertEqual(self.test_book.state, 'available',
#                 'Book state should changed to available')

#     def test_button_lost(self):
#         """Make lost button"""
#         self.test_book.make_lost()
#         self.assertEqual(self.test_book.state, 'lost',
#                 'Book state should changed to lost')