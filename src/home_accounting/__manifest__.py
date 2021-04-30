# -*- coding: utf-8 -*-
{
    'name': "Home accounting",  # Module title
    'summary': "Manage income and expenses easily",  # Module subtitle phrase
    'description': """App for management of income and expenses at home""",
    'author': "Inessa Petrova",
    'category': 'Accounting',
    'version': '12.0.1',
    'depends': ['base'],
    # This data files will be loaded at the installation (commented because file is not added in this example)
    'data': [

        'security/groups.xml',
        'security/ir.model.access.csv',

        'views/income.xml',
        'views/expenses.xml',
        'views/expenses_type.xml',
        'views/income_type.xml',
        'views/outcome.xml',
        'views/currency_exchange.xml',
        'views/test_speed.xml',

        'views/home_accounting.xml',
                
        'data/res_currency_data.xml',
        'data/outcome_data.xml',

        'report/outcome_template.xml',
        'report/outcome_report.xml',
    ],
    'installable': True,
    'application': True,
}
