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
        'keychain2',
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'data/metrics.xml',
        'automation/schedule.xml',
        'views/configuration.xml',
        'views/views.xml',
        'views/logs.xml',
        'views/wizard.xml',
        'views/testing.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': ['static/src/xml/cerp_views.xml'],
    'installable': True,
    'application': False
}
