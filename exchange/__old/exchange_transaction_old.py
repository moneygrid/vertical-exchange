# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Lucas Huber, Copyright: CoĐoo Project
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api
from openerp.exceptions import except_orm

#    List of transactions model entries

class ExchangeAccountingEntry(models.Model):

    _name = 'exchange.transaction'
    _description = 'Exchange Accounting Entries'
    name = fields.Char('Number', required=True, copy=False)
    ref = fields.Char('Reference', copy=False)
    period_id = fields.Many2one('account.period', 'Period', required=True,
                                states={'posted =[('readonly',True)]})
    journal_id = fields.Many2one('account.journal', 'Journal', required=True,
                                 states={'posted =[('readonly',True)]})
    state = fields.Selection(
        [('draft','Unposted'), ('posted','Posted')], 'Status',
        required=True, readonly=True, copy=False,
        help='All manually created new journal entries are usually in the status \'Unposted\', '
             'but you can set the option to skip that status on the related journal. '
             'In that case, they will behave as journal entries automatically created by the '
             'system on document validation (invoices, bank statements...) and will be created '
             'in \'Posted\' status.'),
    line_id = fields.One2many('account.move.line', 'move_id', 'Entries',
        states={'posted =[('readonly',True)]},

    reversal_id = fields.Char('Reversal Entry')
    to_be_reversed = fields.Boolean('To Be Reversed')

    to_check = fields.Boolean('To Review', help='Check this box if you are unsure of that journal entry and if you want to note it as \'to be reviewed\' by an accounting expert.'),
               partner_id = fields.Related('line_id', 'partner_id', type="many2one", relation="res.partner", string="Partner", store={
        _name: (lambda self, cr,uid,ids,c: ids, ['line_id'], 10)
        'account.move.line = (_get_move_from_lines, ['partner_id'],10)
    }),
    amount = fields.Function(_amount_compute, string='Amount', digits_compute=dp.get_precision('Account'), type='float', fnct_search=_search_amount),
                                     date = fields.date('Date', required=True, states={'posted =[('readonly',True)]}, select=True),
    narration =fields.Text('Internal Note'), \
               company_id = fields.related('journal_id','company_id',type='many2one',relation='res.company',string='Company', store=True, readonly=True), \
                            balance = fields.Float('balance', digits_compute=dp.get_precision('Account'), help="This is a field only used for internal purpose and shouldn't be displayed"),
