# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CurrencyExchange(models.Model):
    _name = 'currency_exchange'
    _description = 'Currency exchange'

    currency_1_id = fields.Many2one(
        comodel_name='res.currency',
        string='First currency',
        required=True,
        domain=lambda self: [('name', 'in', ['BYN', 'USD', 'RUB', 'ILS'])],
    )
    """ Первая валюта """

    amount_1 = fields.Float(
            string='First currency amount',
            required=True,
            digits=(16, 2),
        )
    """Сумма в первой валюте"""

    currency_2_id = fields.Many2one(
        comodel_name='res.currency',
        string='Second currency',
        required=True,
        domain=lambda self: [('name', 'in', ['BYN', 'USD', 'RUB', 'ILS'])],
    )
    """ Вторая валюта """

    amount_2 = fields.Float(
            string='Second currency amount',
            required=True,
            digits=(16, 2),
        )
    """ Сумма во второй валюте """

    date_receipt = fields.Date(
        string='Receipt Date',
        required=True,
        default=fields.Date.today()
    )
    """ Дата операции """

    @api.onchange('currency_1_id')
    def onchange_currency_1_id(self):
        if self.currency_1_id and self.currency_1_id == self.currency_2_id:
            self.currency_2_id = False

    @api.onchange('currency_2_id')
    def onchange_currency_2_id(self):
        if self.currency_2_id and self.currency_2_id == self.currency_1_id:
            self.currency_1_id = False
