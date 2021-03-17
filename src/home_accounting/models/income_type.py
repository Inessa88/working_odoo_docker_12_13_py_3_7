# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class IncomeType(models.Model):
    _name = 'income_type'
    _description = 'Income type'

    name = fields.Char(
        string='Income_type',
        required=True,
    )

    _sql_constraints = [
            ('name_uniq',
                'UNIQUE (name)',
                'Income type must be unique.')
    ]

    @api.multi
    def unlink(self):
        if self.env['income'].search_count([
            ('income_type_id', 'in', self.ids)
        ]):
            raise UserError(_(
                'In order to delete an income type, '
                'you must first delete income item.'))
        return super().unlink()
