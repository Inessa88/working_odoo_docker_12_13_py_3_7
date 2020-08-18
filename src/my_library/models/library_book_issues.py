# -*- coding: utf-8 -*-
from odoo import models, fields


class LibraryBookIssues(models.Model):
    _name = 'book.issue'

    book_id = fields.Many2one('library.book', required=True)
    submitted_by = fields.Many2one('res.users')
    issue_description = fields.Text()
