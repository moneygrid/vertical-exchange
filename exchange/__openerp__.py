# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber, Yannick Buron>
# based on account_wallet by Yannick Buron, Copyright Yannick Buron
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Exchange / Community Banking',
    'version': '9.0.0.1.x',
    'category': 'Exchange',
    'author': 'Lucas Huber, moneygrid Project',
    'license': 'LGPL-3',
    'summary': 'Community Exchange/Wallet Backend',
    'website': 'https://github.com/moneygrid/vertical-exchange',
    'depends': [
                'account_accountant',
                'base_exchange',
                'exchange_provider',
                'exchange_provider_internal',
                ],

    'data': [
        # 'security/exchange_security.xml',
        #  'security/ir.model.access.csv',
        'views/exchange_account_view.xml',
        'views/exchange_transaction_view.xml',
        #       'test_view.xml',
        # 'views/exchange_transaction_workflow.xml',
        # 'data/exchange_data.xml',
        # 'data/account_data.xml',
            ],
    """
    'demo': ['demo/exchange_demo.xml'],
    'test': [
        'tests/account_wallet_users.yml',
        'tests/account_wallet_rights.yml',
        'tests/account_wallet_moderator.yml',
        'tests/account_wallet_external.yml',
        'tests/account_wallet_limits.yml',
        'tests/account_wallet_balances.yml',
    ],
    """
    'installable': True,
    'application': True,
}
