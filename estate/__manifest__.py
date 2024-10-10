{
    'name': 'Real Estate',
    'version': '1.0',
    'summary': 'Module for managing real estate properties',
    'description': """
        This module allows users to advertise properties, including features such as:
        - Adding properties
        - Removing properties
        - Viewing available properties
        - Managing sales
    """,
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}