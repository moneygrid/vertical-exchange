# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Distributed database API',
    'version': '9.0.0.1.x',
    'category': 'Exchange',
    'summary': 'Basic framework API for distributed ledgers',
    'author': 'Lucas Huber, moneygrid Project',
    'license': 'LGPL-3',
    'website': 'https://github.com/moneygrid/vertical-exchange',
 #   'description': ''

    'depends': ['base_exchange'],
    'data': [
        'security/ir.model.access.csv',
        'distributed_db_view.xml',
  #      'distributed_db_workflow.xml',
    ],
    "installable": True,
}
