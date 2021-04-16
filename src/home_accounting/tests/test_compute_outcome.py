from odoo.tests.common import TransactionCase
from odoo.tests import tagged


# используем tag для того, чтобы тесты не запускались до установки, т.к. мы обновляем модуль, а не устанавливаем его
@tagged('-at_install', 'post_install') 
class TestComputeOutcome(TransactionCase):

    # удаляем все записи в нашей базе данных перед тестом, а потом после теста они возвращаются, так как
    # все действия откатываются после проведения теста
    def setUp(self, *args, **kwargs):
        super(TestComputeOutcome, self).setUp(*args, **kwargs)
        self.env['income'].search([]).unlink()
        self.env['expenses'].search([]).unlink()
        self.env['currency_exchange'].search([]).unlink()
        # создаем виды доходов и расходов для теста
        self.test_income_type = self.env['income_type'].create({
                'name': 'test_income_type'
            })
        self.test_expenses_type = self.env['expenses_type'].create({
                'name': 'test_expenses_type'
            })
        # создаем по одному доходу и расходу для теста для каждой валюты
        # весь метод - это environment, где мы описываем все наши параметры, которые будут неизменными 
        # для всех тестов, которые будут идти ниже
        self.env['income'].create({'income_type_id': self.test_income_type.id,  'amount_byn': 1000.0},)    
        self.env['expenses'].create({'expenses_type_id': self.test_expenses_type.id,  'amount_byn': 938.0},)
        self.env['income'].create({'income_type_id': self.test_income_type.id,  'amount_usd': 1000.0},)    
        self.env['expenses'].create({'expenses_type_id': self.test_expenses_type.id,  'amount_usd': 937.0},)
        self.env['income'].create({'income_type_id': self.test_income_type.id,  'amount_ils': 1000.0},)    
        self.env['expenses'].create({'expenses_type_id': self.test_expenses_type.id,  'amount_ils': 936.0},)
        self.env['income'].create({'income_type_id': self.test_income_type.id,  'amount_rub': 1000.0},)    
        self.env['expenses'].create({'expenses_type_id': self.test_expenses_type.id,  'amount_rub': 935.0},)
        # когда создаем записи в модели currency_exchange в currency_1_id используем self.env.ref('base.BYN').id по каждой валюте.
        # В данном случае мы ищем реальную id через xml id в БД, которая создается из xml файла при установке модуля 
        self.env['currency_exchange'].create({'date_receipt': '2021-04-15', 'currency_1_id': self.env.ref('base.BYN').id, 'amount_1': 100, 'currency_2_id': self.env.ref('base.USD').id, 'amount_2': 50 },)
        self.env['currency_exchange'].create({'date_receipt': '2021-04-15', 'currency_1_id': self.env.ref('base.USD').id, 'amount_1': 100, 'currency_2_id': self.env.ref('base.ILS').id, 'amount_2': 50 },)
        self.env['currency_exchange'].create({'date_receipt': '2021-04-15', 'currency_1_id': self.env.ref('base.ILS').id, 'amount_1': 100, 'currency_2_id': self.env.ref('base.RUB').id, 'amount_2': 50 },)
        self.env['currency_exchange'].create({'date_receipt': '2021-04-15', 'currency_1_id': self.env.ref('base.RUB').id, 'amount_1': 100, 'currency_2_id': self.env.ref('base.BYN').id, 'amount_2': 50 },)


        # в последних 4 строчках проверяем наш тест, 12.0, 13.0, 14.0, 15.0 в данном случае определяем самостоятельно, в зависимости от ввоздимых выше данных
    def test_compute_outcome(self):
        """Compute outcome in all currencies"""
        final_result = self.env['outcome'].search([])
        self.assertEqual(final_result.outcome_byn, 12.0, 'Wrong outcome in BYN')
        self.assertEqual(final_result.outcome_usd, 13.0, 'Wrong outcome in USD')
        self.assertEqual(final_result.outcome_ils, 14.0, 'Wrong outcome in ILS')
        self.assertEqual(final_result.outcome_rub, 15.0, 'Wrong outcome in RUB')

