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

    currency_id_byn = fields.Many2one(
        'res.currency',
        string='Currency BYN',
        default=lambda self: self.env.ref('base.BYN'),
        )

    amount_byn = fields.Monetary(
        string='Amount BYN',
        currency_field='currency_id_byn',
        )
    """ Сумма расходов в белорусских рублях """

    currency_id_usd = fields.Many2one(
        'res.currency',
        string='Currency USD',
        default=lambda self: self.env.ref('base.USD'),
        )

    amount_usd = fields.Monetary(
        string='Amount USD',
        currency_field='currency_id_usd',
        )
    """ Сумма расходов в долларах США """

    currency_id_ils = fields.Many2one(
        'res.currency',
        string='Currency ILS',
        default=lambda self: self.env.ref('base.ILS'),
        )

    amount_ils = fields.Monetary(
        string='Amount ILS',
        currency_field='currency_id_ils',
        )
    """ Сумма расходов в израильских шеккелях """

    currency_id_rub = fields.Many2one(
        'res.currency',
        string='Currency RUB',
        default=lambda self: self.env.ref('base.RUB'),
        )

    amount_rub = fields.Monetary(
        string='Amount RUB',
        currency_field='currency_id_rub',
        )
    """ Сумма расходов в российских рублях """

   
