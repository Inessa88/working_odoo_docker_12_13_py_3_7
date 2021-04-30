# 1 : imports of python lib
import logging

# 2 :  imports of odoo
from odoo import models, api  # noqa

# 3 :  imports of odoo modules

# 4 :  imports from custom modules
# from odoo.addons.prs_store.tools.utils.price_in_russian import decimal_to_russian_text

_logger = logging.getLogger(__name__)


class OutcomeTemplate(models.AbstractModel):
    """
    Расширение модели, ответственной за формирование отчёта 'home_accounting.outcome_template'
    """

    _name = 'report.home_accounting.outcome_template'
    _description = 'Outcome template report'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']
        report = report_obj._get_report_from_name('home_accounting.outcome_template')
        docs = self.env['outcome'].browse(docids)

        docargs = {
            'data': data,
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs,
            'income_data_for_report': self._income_data_for_report(),
            'expenses_data_for_report': self._expenses_data_for_report(),
        }
        return docargs

    @api.model
    def _income_data_for_report(self):
        # Создаем словарь, который мы должны получить в результате с данными (или без)
        income_data_dict = {}
        # Ищем все записи в модели income
        all_income_records = self.env['income'].search([])
        # Создаем пустой список по годам
        income_years = []
        # Добавляем в данный пустой список годы, которые мы получаем в результате условия
        # по которому из списка всех записей, который мы получили ранее мы выбираем те,
        # у который есть дата и она не была добавлена ранее 
        for unique_date in set(all_income_records.mapped('date_receipt')):
            if unique_date.year not in income_years:
                income_years.append(unique_date.year)
        # Сортируем получившийся список с годами
        income_years.sort()
        for year in income_years:
            # Для каждого года из списка мы фильтруем все записи одного года с одинаковой валютой (по каждой валюте)
            current_year_income_records = all_income_records.filtered(lambda r: r.date_receipt.year == year)
            current_year_income_records_byn = current_year_income_records.filtered(lambda r: r.amount_byn)
            current_year_income_records_usd = current_year_income_records.filtered(lambda r: r.amount_usd)
            current_year_income_records_ils = current_year_income_records.filtered(lambda r: r.amount_ils)
            current_year_income_records_rub = current_year_income_records.filtered(lambda r: r.amount_rub)

            # Используем метод _get_income_type_data_list для того, чтобы получить по каждой валюте список
            # из видов доходов
            byn_income_type_data_list = self._get_income_type_data_list("_byn", current_year_income_records_byn)
            # Получаем income_data_dict, который состоит из ключа (года и международного символа валюты) и значения,
            # в котором будет список из tuples из имени вида дохода и суммы по этому виду дохода за данный год
            income_data_dict[str(year) + ", " + self.env.ref('base.BYN').symbol] = byn_income_type_data_list
            usd_income_type_data_list = self._get_income_type_data_list("_usd", current_year_income_records_usd)
            income_data_dict[str(year) + ", " + self.env.ref('base.USD').symbol] = usd_income_type_data_list
            ils_income_type_data_list = self._get_income_type_data_list("_ils", current_year_income_records_ils)
            income_data_dict[str(year) + ", " + self.env.ref('base.ILS').symbol] = ils_income_type_data_list
            rub_income_type_data_list = self._get_income_type_data_list("_rub", current_year_income_records_rub)
            income_data_dict[str(year) + ", " + self.env.ref('base.RUB').symbol] = rub_income_type_data_list
        # Получаем наш словарь, который и будем использовать в outcome_template.xml
        return income_data_dict

    # Создаем метод для получения списка из записей по видам доходов, которые будем использовать в методе,
    # указанном выше
    @api.model
    def _get_income_type_data_list(self, curr_field_ending, current_year_income_curr_records=None):
        # определяем сумму всех доходов за год по одной валюте, current_year_income_curr_records - это записи в БД
        all_incomes_per_year = sum([record["amount" + curr_field_ending] for record in current_year_income_curr_records])
        income_types = set(current_year_income_curr_records.mapped('income_type_id'))
        # Создаем пустой список, который будем дополнять в процессе и выведем в конце метода
        income_type_data_list = []
        # Здесь записи с определенными видами доходов, которые есть у нас в системеб мы фильтруем
        # по каждому виду отдельно.
        for income_type in income_types:
            recs_with_current_inc_type = current_year_income_curr_records.filtered(
                lambda r: r.income_type_id == income_type
            )
            # Считаем сумму по виду дохода по полю amount_byn и другим видам валют из модели income
            # для каждой записи из получившегося списка записей с определенным видом дохода
            income_type_amount = sum([record["amount" + curr_field_ending] for record in recs_with_current_inc_type])
            # рассчитываем удельный вес каждого вида доходов, также определяем условие, что он считается если сумма по доходу не равна 0
            # округляем результат с помощью функции round
            income_type_percent = round(income_type_amount / all_incomes_per_year * 100, 0) if all_incomes_per_year else 0
            # В пустой список добавляем получившиеся название вида дохода, сумму по нему и удельный вес
            income_type_data_list.append((income_type.name, income_type_amount, income_type_percent))
        #  В результате получаем список из записей в которых есть название вида дохода и сумма по этому виду
        # дохода по требуемой валюте, которую указываем в начале метода
        return income_type_data_list

    # Здесь таким же способом как и выше получаем словарь для модели expenses по таким же этапам
    @api.model
    def _expenses_data_for_report(self):
            expenses_data_dict = {}
            all_expenses_records = self.env['expenses'].search([])
            expenses_years = []
            for unique_date in set(all_expenses_records.mapped('date_receipt')):
                if unique_date.year not in expenses_years:
                    expenses_years.append(unique_date.year)
            expenses_years.sort()
            for year in expenses_years:
                current_year_expenses_records = all_expenses_records.filtered(lambda r: r.date_receipt.year == year)
                current_year_expenses_records_byn = current_year_expenses_records.filtered(lambda r: r.amount_byn)
                current_year_expenses_records_usd = current_year_expenses_records.filtered(lambda r: r.amount_usd)
                current_year_expenses_records_ils = current_year_expenses_records.filtered(lambda r: r.amount_ils)
                current_year_expenses_records_rub = current_year_expenses_records.filtered(lambda r: r.amount_rub)
                byn_expenses_type_data_list = self._get_expenses_type_data_list("_byn", current_year_expenses_records_byn)
                expenses_data_dict[str(year) + ", " + self.env.ref('base.BYN').symbol] = byn_expenses_type_data_list
                usd_expenses_type_data_list = self._get_expenses_type_data_list("_usd", current_year_expenses_records_usd)
                expenses_data_dict[str(year) + ", " + self.env.ref('base.USD').symbol] = usd_expenses_type_data_list
                ils_expenses_type_data_list = self._get_expenses_type_data_list("_ils", current_year_expenses_records_ils)
                expenses_data_dict[str(year) + ", " + self.env.ref('base.ILS').symbol] = ils_expenses_type_data_list
                rub_expenses_type_data_list = self._get_expenses_type_data_list("_rub", current_year_expenses_records_rub)
                expenses_data_dict[str(year) + ", " + self.env.ref('base.RUB').symbol] = rub_expenses_type_data_list
            return expenses_data_dict    


    @api.model
    def _get_expenses_type_data_list(self, curr_field_ending, current_year_expenses_curr_records=None):
        all_expenses_per_year = sum([record["amount" + curr_field_ending] for record in current_year_expenses_curr_records])
        expenses_types = set(current_year_expenses_curr_records.mapped('expenses_type_id'))
        expenses_type_data_list = []
        for expenses_type in expenses_types:
            recs_with_current_exp_type = current_year_expenses_curr_records.filtered(
                lambda r: r.expenses_type_id == expenses_type
            )
            expenses_type_amount = sum([record["amount" + curr_field_ending] for record in recs_with_current_exp_type])
            expenses_type_percent = round(expenses_type_amount / all_expenses_per_year * 100, 0) if all_expenses_per_year else 0
            expenses_type_data_list.append((expenses_type.name, expenses_type_amount, expenses_type_percent))
        return expenses_type_data_list
