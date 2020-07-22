# -*- coding: utf-8 -*-

{
    'name': "Cloud ERP AWS (basic)",

    'summary': """
        Manage costs and usage of AWS""",

    'description': """
        Long description of module's purpose
    """,
    'author': "Cloud ERP",
    'website': "http://cerp.cloud/aws",
    'category': 'Specific Industry Applications',
    'version': '0.0.1',
    'depends': ['cerp_core'],
    'sequence': '1000',
    'external_dependencies': {
        'python': [
            'boto3'
        ],
    },
    'data': [
        'data/metrics.xml'
    ],
    'installable': True,
    'application': False
}
