{
    'name': "My library",
    'summary': "Manage books easily",
    'description': """Long description""",
    'author': "Your name",
    'website': "http://www.example.com",
    'category': 'Library',
    'version': '12.0.1',
    'depends': ['base', 'decimal_precision'],
    'data': [
            'security/groups.xml',
            'security/library_security.xml',
            'security/ir.model.access.csv',
            'views/library_book.xml',
            'views/library_book_rent.xml',
            'views/library_book_rent_wizard.xml',
            'views/library_book_return_wizard.xml',
            'views/library_book_statistics.xml',
            'views/res_config_settings_views.xml',
            'views/res_config_settings.xml',
            'data/data.xml',
            'data/library_stage.xml',
    ],
    'demo': [
            'data/demo.xml',
    ],
    'post_init_hook': 'add_book_hook',
}