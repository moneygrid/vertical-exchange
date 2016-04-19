# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    'name': 'Exchange Provider Internal',
    'version': '9.0.0.1.x',
    'category': 'Exchange',
    'summary': 'for the internal transaction engine',
    'author': 'Lucas Huber, moneygrid Project',
    'license': 'LGPL-3',
    'website': 'https://github.com/moneygrid/vertical-exchange',
    'description':
        """
        Dumy Exchange Provider to use the internal transaction engine
        """,
    'depends': ['base_exchange',
                'exchange_provider'],
    'data': [
        'views/exchange_provider_view.xml',
        'data/internal_data.xml',
        'data/account_data.xml',
    ],
    'installable': True,
}
