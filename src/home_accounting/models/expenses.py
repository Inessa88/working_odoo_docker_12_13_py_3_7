# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Expenses(models.Model):
    _name = 'expenses'
    _description = 'Expenses'

    expenses_type_id = fields.Many2one(
        string='Expenses',
        comodel_name='expenses_type',
        required=True,
    )
    """ Тип источника расходов """

    date_receipt = fields.Date(
        string='Receipt Date',
        required=True,
        default=fields.Date.today,
    )
    """ Дата операции """

    amount = fields.Float(
        string='Amount',
        required=True,
        digits=(16, 2),
    )
    """ Сумма расходов """
