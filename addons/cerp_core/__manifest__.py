# -*- coding: utf-8 -*-
{
    'name': "Cloud ERP",

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
        'base',
        'keychain2',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/metrics.xml',
        'automation/schedule.xml',
        'views/views.xml',
        'views/configuration.xml',
        'views/logs.xml',
        'views/testing.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': False
}
