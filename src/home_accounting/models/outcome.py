# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Outcome(models.Model):
    _name = 'outcome'
    _description = 'Outcome'

    name = fields.Char(
        string='Name',
        required=True,
    )
    
    currency_id_byn = fields.Many2one(
        'res.currency', string='Currency BYN',
        compute='_compute_outcome',
        )

    outcome_byn = fields.Monetary(
        string='Outcome BYN',
        currency_field='currency_id_byn',
        compute='_compute_outcome',
        readonly=True,
        )
    """ Результат в белорусских рублях """

    currency_id_usd = fields.Many2one(
        'res.currency', string='Currency USD',
        compute='_compute_outcome',
        )

    outcome_usd = fields.Monetary(
        string='Outcome USD',
        currency_field='currency_id_usd',
        compute='_compute_outcome',
        readonly=True,
        )
    """ Результат в долларах США """

    currency_id_ils = fields.Many2one(
        'res.currency', string='Currency ILS',
        compute='_compute_outcome',
        )

    outcome_ils = fields.Monetary(
        string='Outcome ILS',
        currency_field='currency_id_ils',
        compute='_compute_outcome',
        readonly=True,
        )
    """ Результат в израильских шеккелях """

    currency_id_rub = fields.Many2one(
        'res.currency', string='Currency RUB',
        compute='_compute_outcome',
        )

    outcome_rub = fields.Monetary(
        string='Outcome RUB',
        currency_field='currency_id_rub',
        compute='_compute_outcome',
        readonly=True,
        )
    """ Результат в российских рублях """

    def _compute_outcome(self):
        for record in self:
            sql_query = """
                SELECT
                sum(amount_byn) AS all_incomes_byn, sum(amount_usd) AS all_incomes_usd,
                sum(amount_ils) AS all_incomes_ils, sum(amount_rub) AS all_incomes_rub
                FROM income
            """
            self.env.cr.execute(sql_query)
            result = self.env.cr.fetchall()
            all_incomes_byn, all_incomes_usd, all_incomes_ils, all_incomes_rub = result[0]
            all_incomes_byn = all_incomes_byn or 0.0
            all_incomes_usd = all_incomes_usd or 0.0
            all_incomes_ils = all_incomes_ils or 0.0
            all_incomes_rub = all_incomes_rub or 0.0
            # Определение сумм доходов по четырем валютам. Финальная строчка - это присвоение каждого элемента финального tuple каждой валюте.
            # Т.к. выводимый результат - это tuple, который содержит 4 цифры - доходы по каждой валюте.
            sql_query = """
                SELECT
                sum(amount_byn) AS all_expenses_byn, sum(amount_usd) AS all_expenses_usd,
                sum(amount_ils) AS all_expenses_ils, sum(amount_rub) AS all_expenses_rub
                FROM expenses
            """
            self.env.cr.execute(sql_query)
            result = self.env.cr.fetchall()
            all_expenses_byn, all_expenses_usd, all_expenses_ils, all_expenses_rub = result[0]
            all_expenses_byn = all_expenses_byn or 0.0
            all_expenses_usd = all_expenses_usd or 0.0
            all_expenses_ils = all_expenses_ils or 0.0
            all_expenses_rub = all_expenses_rub or 0.0
             # Определение сумм расходов по четырем валютам. Финальная строчка - это присвоение каждого элемента финального tuple каждой валюте.
            # Т.к. выводимый результат - это tuple, который содержит 4 цифры - расходы по каждой валюте.
            sql_query = """
                SELECT currency_1_id, sum(amount_1) FROM currency_exchange GROUP BY currency_1_id
            """
            self.env.cr.execute(sql_query)
            result = self.env.cr.fetchall()
            amount_dec_ils = 0
            amount_dec_usd = 0
            amount_dec_byn = 0
            amount_dec_rub = 0 
            # присваиваем значения каждой переменной.
            for item in result:
                if item[0] == self.env.ref('base.ILS').id:
                    amount_dec_ils = item[1]
                elif item[0] == self.env.ref('base.USD').id:
                    amount_dec_usd = item[1]
                elif item[0] == self.env.ref('base.BYN').id:
                    amount_dec_byn = item[1]
                elif item[0] == self.env.ref('base.RUB').id:
                    amount_dec_rub = item[1]
            # Здесь определяем сумму уменьшения каждой валюты после обмена валюты.
            # В данном случае в  результат приходит list of tuples, в котором на первом месте стоит currency_id, а на втором
            # сумма в данной валюте. Поэтому цикл проходит 4 раза, чтобы определить суммы по каждой валюте.
            sql_query = """
                SELECT currency_2_id, sum(amount_2) FROM currency_exchange GROUP BY currency_2_id
            """
            self.env.cr.execute(sql_query)
            result = self.env.cr.fetchall()
            amount_inc_ils = 0
            amount_inc_usd = 0
            amount_inc_byn = 0
            amount_inc_rub = 0
            for item in result:
                if item[0] == self.env.ref('base.ILS').id:
                    amount_inc_ils = item[1]
                elif item[0] == self.env.ref('base.USD').id:
                    amount_inc_usd = item[1]
                elif item[0] == self.env.ref('base.BYN').id:
                    amount_inc_byn = item[1]
                elif item[0] == self.env.ref('base.RUB').id:
                    amount_inc_rub = item[1]
            # Здесь определяем сумму увелечения валюты по каждой валюте. Тоже выбираем из list of tuples.
            record.currency_id_byn = self.env.ref('base.BYN').id
            record.currency_id_usd = self.env.ref('base.USD').id
            record.currency_id_ils = self.env.ref('base.ILS').id
            record.currency_id_rub = self.env.ref('base.RUB').id
            record.outcome_byn = all_incomes_byn - all_expenses_byn + amount_inc_byn - amount_dec_byn
            record.outcome_usd = all_incomes_usd - all_expenses_usd + amount_inc_usd - amount_dec_usd
            record.outcome_ils = all_incomes_ils - all_expenses_ils + amount_inc_ils - amount_dec_ils
            record.outcome_rub = all_incomes_rub - all_expenses_rub + amount_inc_rub - amount_dec_rub
            # Расчет итогового результата по каждой валюте.
            
    # def _compute_outcome(self):
    #     for record in self:
    #         all_expenses_BYN = 0
    #         all_incomes_BYN = 0
    #         all_currency_increase_BYN = 0
    #         all_currency_decrease_BYN = 0
    #         for expense in self.env['expenses'].search([]):
    #             all_expenses_BYN += expense.amount_byn
    #         for income in self.env['income'].search([]):
    #             all_incomes_BYN += income.amount_byn
    #         for currency_increase in self.env['currency_exchange'].search([
    #             ('currency_2_id', '=', self.env.ref('base.BYN').id)
    #         ]):
    #             all_currency_increase_BYN += currency_increase.amount_2
    #         for currency_decrease in self.env['currency_exchange'].search([
    #             ('currency_1_id', '=', self.env.ref('base.BYN').id)
    #         ]):
    #             all_currency_decrease_BYN += currency_decrease.amount_1
    #         record.outcome_byn = all_incomes_BYN - all_expenses_BYN + all_currency_increase_BYN - all_currency_decrease_BYN

    #         all_expenses_USD = 0
    #         all_incomes_USD = 0
    #         all_currency_increase_USD = 0
    #         all_currency_decrease_USD = 0
    #         for expense in self.env['expenses'].search([]):
    #             all_expenses_USD += expense.amount_usd
    #         for income in self.env['income'].search([]):
    #             all_incomes_USD += income.amount_usd
    #         for currency_increase in self.env['currency_exchange'].search([
    #             ('currency_2_id', '=', self.env.ref('base.USD').id)
    #         ]):
    #             all_currency_increase_USD += currency_increase.amount_2
    #         for currency_decrease in self.env['currency_exchange'].search([
    #             ('currency_1_id', '=', self.env.ref('base.USD').id)
    #         ]):
    #             all_currency_decrease_USD += currency_decrease.amount_1
    #         record.outcome_usd = all_incomes_USD - all_expenses_USD + all_currency_increase_USD - all_currency_decrease_USD

    #         all_expenses_ILS = 0
    #         all_incomes_ILS = 0
    #         all_currency_increase_ILS = 0
    #         all_currency_decrease_ILS = 0
    #         for expense in self.env['expenses'].search([]):
    #             all_expenses_ILS += expense.amount_ils
    #         for income in self.env['income'].search([]):
    #             all_incomes_ILS += income.amount_ils
    #         for currency_increase in self.env['currency_exchange'].search([
    #             ('currency_2_id', '=', self.env.ref('base.ILS').id)
    #         ]):
    #             all_currency_increase_ILS += currency_increase.amount_2
    #         for currency_decrease in self.env['currency_exchange'].search([
    #             ('currency_1_id', '=', self.env.ref('base.ILS').id)
    #         ]):
    #             all_currency_decrease_ILS += currency_decrease.amount_1
    #         record.outcome_ils = all_incomes_ILS - all_expenses_ILS + all_currency_increase_ILS - all_currency_decrease_ILS

    #         all_expenses_RUB = 0
    #         all_incomes_RUB = 0
    #         all_currency_increase_RUB = 0
    #         all_currency_decrease_RUB = 0
    #         for expense in self.env['expenses'].search([]):
    #             all_expenses_RUB += expense.amount_rub
    #         for income in self.env['income'].search([]):
    #             all_incomes_RUB += income.amount_rub
    #         for currency_increase in self.env['currency_exchange'].search([
    #             ('currency_2_id', '=', self.env.ref('base.RUB').id)
    #         ]):
    #             all_currency_increase_RUB += currency_increase.amount_2
    #         for currency_decrease in self.env['currency_exchange'].search([
    #             ('currency_1_id', '=', self.env.ref('base.RUB').id)
    #         ]):
    #             all_currency_decrease_RUB += currency_decrease.amount_1
    #         record.outcome_rub = all_incomes_RUB - all_expenses_RUB + all_currency_increase_RUB - all_currency_decrease_RUB
    
    @api.model
    def make_currency_active(self):
        self = self.with_context(active_test=False)
        currencies_to_activate = self.env['res.currency'].search([
            ('name', 'in', ['BYN', 'USD', 'RUB', 'ILS'])
        ])
        currencies_to_activate.write({
            'active': True,
        })
