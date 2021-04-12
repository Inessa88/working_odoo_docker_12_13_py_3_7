# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TestSpeed(models.TransientModel):
    _name = 'test_speed'
    _description = 'Test final outcome calculation speed '

    def create_test_data(self):
        number_of_records_to_create = self.env.context.get('record_number')
        income_vals = []
        expenses_vals = []
        test_income_type = self.env['income_type'].search([('name', '=', 'test_income_type')])
        if not test_income_type:
            test_income_type = self.env['income_type'].create({
                'name': 'test_income_type'
            })
        test_expenses_type = self.env['expenses_type'].search([('name', '=', 'test_expenses_type')])
        if not test_expenses_type:
            test_expenses_type = self.env['expenses_type'].create({
                'name': 'test_expenses_type'
            })
        for item in range(number_of_records_to_create):
            income_vals.append({'income_type_id': test_income_type.id,  'amount_byn': 1000},)
            expenses_vals.append({'expenses_type_id': test_expenses_type.id,  'amount_byn': 1000},)
        self.env['income'].create(income_vals)    
        self.env['expenses'].create(expenses_vals)

    def delete_all_test_data(self):
        test_income_type = self.env['income_type'].search([('name', '=', 'test_income_type')])
        self.env['income'].search([('income_type_id','=',test_income_type.id)]).unlink()
        test_expenses_type = self.env['expenses_type'].search([('name', '=', 'test_expenses_type')])
        self.env['expenses'].search([('expenses_type_id','=',test_expenses_type.id)]).unlink()
        test_income_type.unlink()
        test_expenses_type.unlink()