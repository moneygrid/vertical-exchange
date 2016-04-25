# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber, Yannick Buron>
# based on account_wallet by Yannick Buron, Copyright Yannick Buron
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Exchange / Community Banking',
    'version': '9.0.0.1.x',
    'category': 'Exchange Loan',
    'author': 'Lucas Huber, moneygrid Project',
    'license': 'LGPL-3',
    'summary': 'Exchange Loan/Contract Module',
    'description': """
 Exchange Loan Module
 ====================

 Allow members to get loans and contracts and perform the necessary transactions between the contracted accounts.

 -----------------------------------------------------
 """,
    'website': 'https://github.com/moneygrid/vertical-exchange',
    'depends': [
                'exchange',
                'exchange_provider',
                'exchange_provider_internal',
                ],

    'data': [
        'security/ir.model.access.csv',
        'views/res_config_view.xml',
        'views/exchange_transaction_view.xml',
        'views/exchange_loan_view.xml',
        'data/loan_data.xml',
            ],
    'installable': True,
    'application': False,
}
