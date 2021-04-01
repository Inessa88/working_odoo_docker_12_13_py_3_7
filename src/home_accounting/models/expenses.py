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
        default=fields.Date.today(),
    )
    """ Дата операции """

    currency_id_BYN = fields.Many2one(
        'res.currency',
        string='Currency BYN',
        default=lambda self: self.env.ref('base.BYN'),
        )

    amount_BYN = fields.Monetary(
        string='Amount BYN',
        currency_field='currency_id_BYN',
        )
    """ Сумма расходов в белорусских рублях """

    currency_id_USD = fields.Many2one(
        'res.currency',
        string='Currency USD',
        default=lambda self: self.env.ref('base.USD'),
        )

    amount_USD = fields.Monetary(
        string='Amount USD',
        currency_field='currency_id_USD',
        )
    """ Сумма расходов в долларах США """

    currency_id_ILS = fields.Many2one(
        'res.currency',
        string='Currency ILS',
        default=lambda self: self.env.ref('base.ILS'),
        )

    amount_ILS = fields.Monetary(
        string='Amount ILS',
        currency_field='currency_id_ILS',
        )
    """ Сумма расходов в израильских шеккелях """

    currency_id_RUB = fields.Many2one(
        'res.currency',
        string='Currency RUB',
        default=lambda self: self.env.ref('base.RUB'),
        )

    amount_RUB = fields.Monetary(
        string='Amount RUB',
        currency_field='currency_id_RUB',
        )
    """ Сумма расходов в российских рублях """

   
