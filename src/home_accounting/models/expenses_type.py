# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ExpensesType(models.Model):
    _name = 'expenses_type'
    _description = 'Expenses type'

    name = fields.Char(
        string='Expenses type',
        required=True,
    )
    """ Название вида расходов """

    _sql_constraints = [
        ('name_uniq',
            'UNIQUE (name)',
            'Expenses type must be unique.')
    ]

    @api.multi
    def unlink(self):
        if self.env['expenses'].search_count([
            ('expenses_type_id', 'in', self.ids)
        ]):
            raise UserError(_(
                'In order to delete an expenses type, you '
                'must first delete an expenses item.'
            ))
        return super().unlink()
