# -*- coding: utf-8 -*-
{
    'name': "Cloud ERP (basic)",

    'summary': """
        Manage costs and usage of cloud service providers""",

    'description': """
        Long description of module's purpose
    """,
    'author': "Cloud ERP",
    'website': "http://cerp.cloud",
    'category': 'Specific Industry Applications',
    'version': '0.1',
    'depends': [
        'cerp_core',
        'web_tour'
    ],
    'data': [
        'views/views.xml',
        'views/tours.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True
}
