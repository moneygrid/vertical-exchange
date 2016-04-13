# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Exchange Provider Dumy',
    'version': '9.0.0.1.x',
    'category': 'Exchange',
    'summary': 'Dumy API for distributed ledgers',
    'author': 'Lucas Huber, moneygrid Project',
    'license': 'LGPL-3',
    'website': 'https://github.com/moneygrid/vertical-exchange',
    'description': """
This module can be used as template to integrate future Exchange Provider into the Odoo Exchange framework""",
    'depends': ['base_exchange'],
    'data': [
        # 'views/dumy_button_view.xml',
        'views/exchange_provider_view.xml',
        'data/dumy_data.xml',
    ],
    'installable': True,
}
