from . import library_book
from . import library_book_rent
from odoo import api, fields, SUPERUSER_ID
from . import res_config_settings


def add_book_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    book_data1 = {'name': 'Book 1', 'date_release': fields.Date.today()}
    book_data2 = {'name': 'Book 2', 'date_release': fields.Date.today()}
    env['library.book'].create([book_data1, book_data2])
    