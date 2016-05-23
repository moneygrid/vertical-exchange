# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber, Yannick Buron>
# based on account_wallet by Yannick Buron, Copyright Yannick Buron
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Exchange Membership',
    'version': '9.0.0.1.x',
    'category': 'Association',
    'summary': 'Community Exchange Membership integration',
    'author': 'Lucas Huber, moneygrid Project',
    'license': 'LGPL-3',
    'description': """
Exchange Membership
===================

Add Exchange management forms to the association part of Odoo
-------------------------------------------------------------
    * Adding state buttons to Partner
    * Adding the wallet page to Partner
    *
""",
    'website': 'https://github.com/moneygrid/vertical-exchange',
    'depends': ['membership',
                'exchange_provider'
    ],
    'data': [
 #       'security/membership_users_security.xml',
 #       'security/ir.model.access.csv',
        'exchange_membership_view.xml'
    ],
    'installable': True,
}
