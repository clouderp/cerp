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
    'external_dependencies': {
        'python': [
            'boto3'
        ],
    },
    'installable': True,
    'application': False,
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
}
