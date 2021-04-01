# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Outcome(models.Model):
    _name = 'outcome'
    _description = 'Outcome'

    name = fields.Char(
        string='Name',
        required=True,
    )
    
    currency_id_BYN = fields.Many2one(
        'res.currency', string='Currency BYN',
        )

    outcome_BYN = fields.Monetary(
        string='Outcome BYN',
        currency_field='currency_id_BYN',
        compute='_compute_outcome',
        readonly=True,
        )
    """ Результат в белорусских рублях """

    currency_id_USD = fields.Many2one(
        'res.currency', string='Currency USD',
        )

    outcome_USD = fields.Monetary(
        string='Outcome USD',
        currency_field='currency_id_USD',
        compute='_compute_outcome',
        readonly=True,
        )
    """ Результат в долларах США """

    currency_id_ILS = fields.Many2one(
        'res.currency', string='Currency ILS',
        )

    outcome_ILS = fields.Monetary(
        string='Outcome ILS',
        currency_field='currency_id_ILS',
        compute='_compute_outcome',
        readonly=True,
        )
    """ Результат в израильских шеккелях """

    currency_id_RUB = fields.Many2one(
        'res.currency', string='Currency RUB',
        )

    outcome_RUB = fields.Monetary(
        string='Outcome RUB',
        currency_field='currency_id_RUB',
        compute='_compute_outcome',
        readonly=True,
        )
    """ Результат в российских рублях """

    def _compute_outcome(self):
        for record in self:
            all_expenses_BYN = 0
            all_incomes_BYN = 0
            all_currency_increase_BYN = 0
            all_currency_decrease_BYN = 0
            for expense in self.env['expenses'].search([]):
                all_expenses_BYN += expense.amount_BYN
            for income in self.env['income'].search([]):
                all_incomes_BYN += income.amount_BYN
            for currency_increase in self.env['currency_exchange'].search([
                ('currency_2_id', '=', self.env.ref('base.BYN').id)
            ]):
                all_currency_increase_BYN += currency_increase.amount_2
            for currency_decrease in self.env['currency_exchange'].search([
                ('currency_1_id', '=', self.env.ref('base.BYN').id)
            ]):
                all_currency_decrease_BYN += currency_decrease.amount_1
            record.outcome_BYN = all_incomes_BYN - all_expenses_BYN + all_currency_increase_BYN - all_currency_decrease_BYN

            all_expenses_USD = 0
            all_incomes_USD = 0
            all_currency_increase_USD = 0
            all_currency_decrease_USD = 0
            for expense in self.env['expenses'].search([]):
                all_expenses_USD += expense.amount_USD
            for income in self.env['income'].search([]):
                all_incomes_USD += income.amount_USD
            for currency_increase in self.env['currency_exchange'].search([
                ('currency_2_id', '=', self.env.ref('base.USD').id)
            ]):
                all_currency_increase_USD += currency_increase.amount_2
            for currency_decrease in self.env['currency_exchange'].search([
                ('currency_1_id', '=', self.env.ref('base.USD').id)
            ]):
                all_currency_decrease_USD += currency_decrease.amount_1
            record.outcome_USD = all_incomes_USD - all_expenses_USD + all_currency_increase_USD - all_currency_decrease_USD

            all_expenses_ILS = 0
            all_incomes_ILS = 0
            all_currency_increase_ILS = 0
            all_currency_decrease_ILS = 0
            for expense in self.env['expenses'].search([]):
                all_expenses_ILS += expense.amount_ILS
            for income in self.env['income'].search([]):
                all_incomes_ILS += income.amount_ILS
            for currency_increase in self.env['currency_exchange'].search([
                ('currency_2_id', '=', self.env.ref('base.ILS').id)
            ]):
                all_currency_increase_ILS += currency_increase.amount_2
            for currency_decrease in self.env['currency_exchange'].search([
                ('currency_1_id', '=', self.env.ref('base.ILS').id)
            ]):
                all_currency_decrease_ILS += currency_decrease.amount_1
            record.outcome_ILS = all_incomes_ILS - all_expenses_ILS + all_currency_increase_ILS - all_currency_decrease_ILS

            all_expenses_RUB = 0
            all_incomes_RUB = 0
            all_currency_increase_RUB = 0
            all_currency_decrease_RUB = 0
            for expense in self.env['expenses'].search([]):
                all_expenses_RUB += expense.amount_RUB
            for income in self.env['income'].search([]):
                all_incomes_RUB += income.amount_RUB
            for currency_increase in self.env['currency_exchange'].search([
                ('currency_2_id', '=', self.env.ref('base.RUB').id)
            ]):
                all_currency_increase_RUB += currency_increase.amount_2
            for currency_decrease in self.env['currency_exchange'].search([
                ('currency_1_id', '=', self.env.ref('base.RUB').id)
            ]):
                all_currency_decrease_RUB += currency_decrease.amount_1
            record.outcome_RUB = all_incomes_RUB - all_expenses_RUB + all_currency_increase_RUB - all_currency_decrease_RUB

    @api.model
    def make_currency_active(self):
        self = self.with_context(active_test=False)
        currencies_to_activate = self.env['res.currency'].search([
            ('name', 'in', ['BYN', 'USD', 'RUB', 'ILS'])
        ])
        currencies_to_activate.write({
            'active': True,
        })
