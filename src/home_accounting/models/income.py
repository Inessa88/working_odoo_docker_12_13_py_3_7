# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Income(models.Model):
    _name = 'income'
    _description = 'Income'

    income_type_id = fields.Many2one(
        string='Income',
        comodel_name='income_type',
        required=True,
    )
    """ Тип источника дохода """

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
    """ Сумма поступления """
