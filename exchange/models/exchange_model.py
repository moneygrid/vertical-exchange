# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber, Yannick Buron>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from openerp import models, fields, api, _
from openerp.exceptions import except_orm

from datetime import datetime, timedelta
import subprocess
# import paramiko
import os.path
import string
# import errno
import random

from os.path import expanduser

import logging
_logger = logging.getLogger(__name__)


class ExchangeLog(models.Model):
    """
    Define the log object, where is stored the log of the commands after
    we execute an action.
    """

    _name = 'exchange.log'

    @api.one
    def _get_name(self):
        """
        Return the name of the record linked to this log.
        """
        model_obj = self.env[self.model]
        record = model_obj.browse(self.res_id)
        if record and hasattr(record, 'name'):
            self.name = record.name
        return

    model = fields.Char('Related Document Model', size=128, select=1)
    res_id = fields.Integer('Related Document ID', select=1)
    name = fields.Char('Name', compute='_get_name', size=128)
    action = fields.Char('Action', size=64)
    description = fields.Text('Description')
    state = fields.Selection(
        [('unfinished', 'Not finished'), ('ok', 'Ok'), ('ko', 'Ko')],
        'State', required=True, default='unfinished')
    create_date = fields.Datetime('Launch Date')
    finish_date = fields.Datetime('Finish Date')
    expiration_date = fields.Datetime('Expiration Date')

    _order = 'create_date desc'


class ExchangeModel(models.AbstractModel):
    """
    Define the exchange.model abstract object, which is inherited by most
    objects in exchange.
    """

    _name = 'exchange.model'

    _log_expiration_days = 30
    _autodeploy = True

    # We create the name field to avoid warning for the constraints
    name = fields.Char('Name', size=64, required=True)
    log_ids = fields.One2many(
        'exchange.log', 'res_id',
        domain=lambda self: [('model', '=', self._name)],
        auto_join=True, string='Logs')

    @property
    def email_sysadmin(self):
        """
        Property returning the sysadmin email of the exchange.
        """
        return self.env.ref('clouder.clouder_settings').email_sysadmin

    @property
    def user_partner(self):
        """
        Property returning the full name of the server.
        """
        return self.env['res.partner'].search(
            [('user_ids', 'in', int(self.env.uid))])[0]


    @property
    def home_directory(self):
        """
        Property returning the path to the home directory.
        """
        return expanduser("~")

    @property
    def now_date(self):
        """
        Property returning the actual date.
        """
        now = datetime.now()
        return now.strftime("%Y-%m-%d")

    @property
    def now_hour(self):
        """
        Property returning the actual hour.
        """
        now = datetime.now()
        return now.strftime("%H-%M")

    @property
    def now_hour_regular(self):
        """
        Property returning the actual hour.
        """
        now = datetime.now()
        return now.strftime("%H:%M:%S")

    @property
    def now_bup(self):
        """
        Property returning the actual date, at the bup format.
        """
        now = datetime.now()
        return now.strftime("%Y-%m-%d-%H%M%S")

    @api.one
    @api.constrains('name')
    def _check_config(self):
        """
        Check that we specified the sysadmin email in configuration before
        making any action.
        """
        if not self.env.ref('clouder.clouder_settings').email_sysadmin:
            raise except_orm(
                _('Data error!'),
                _("You need to specify the sysadmin email in configuration"))

    @api.multi
    def create_log(self, action):
        """
        Create the log record and add his id in context.

        :param action: The action which trigger the log.
        """
        if 'log_id' in self.env.context:
            return self.env.context

        if 'logs' in self.env.context:
            logs = self.env.context['logs']
        else:
            logs = {}

        if not self._name in logs:
            logs[self._name] = {}
        now = datetime.now()
        if not self.id in logs[self._name]:
            expiration_date = (
                now + timedelta(days=self._log_expiration_days)
            ).strftime("%Y-%m-%d")
            log_id = self.env['exchange.log'].create({
                'model': self._name, 'res_id': self.id,
                'action': action, 'expiration_date': expiration_date})
            logs[self._name][self.id] = {}
            logs[self._name][self.id]['log_model'] = self._name
            logs[self._name][self.id]['log_res_id'] = self.id
            logs[self._name][self.id]['log_id'] = log_id.id
            logs[self._name][self.id]['log_log'] = ''

        self = self.with_context(logs=logs)
        return self.env.context

    @api.multi
    def end_log(self):
        """
        Close the log record if the action finished correctly.
        """
        log_obj = self.env['exchange.log']
        if 'logs' in self.env.context:
            log = log_obj.browse(
                self.env.context['logs'][self._name][self.id]['log_id'])
            if log.state == 'unfinished':
                log.state = 'ok'

    @api.multi
    def log(self, message):
        """
        Add a message in the logs specified in context.

        :param message: The message which will be logged.
        """
        message = filter(lambda x: x in string.printable, message)
        _logger.info(message)
        log_obj = self.env['exchange.log']
        if 'logs' in self.env.context:
            for model, model_vals in self.env.context['logs'].iteritems():
                for res_id, vals in \
                        self.env.context['logs'][model].iteritems():
                    log = log_obj.browse(
                        self.env.context['logs'][model][res_id]['log_id'])
                    log.description = (log.description or '') + message + '\n'

    @api.multi
    def ko_log(self):
        """
        Ko the log specified in context.
        """
        log_obj = self.env['exchange.log']
        if 'logs' in self.env.context:
            for model, model_vals in self.env.context['logs'].iteritems():
                for res_id, vals in \
                        self.env.context['logs'][model].iteritems():
                    log = log_obj.browse(
                        self.env.context['logs'][model][res_id]['log_id'])
                    log.state = 'ko'

    @api.multi
    def deploy(self):
        """
        Hook which can be used by inheriting objects to execute actions when
        we create a new record.
        """
        return

    @api.multi
    def purge(self):
        """
        Hook which can be used by inheriting objects to execute actions when
        we delete a record.
        """
        return

    @api.multi
    def deploy_links(self):
        """
        Force deployment of all links linked to a record.
        """
        if hasattr(self, 'link_ids'):
            for link in self.link_ids:
                link.deploy_()

    @api.multi
    def purge_links(self):
        """
        Force purge of all links linked to a record.
        """
        if hasattr(self, 'link_ids'):
            for link in self.link_ids:
                link.purge_()

    @api.multi
    def reinstall(self):
        """"
        Action which purge then redeploy a record.
        """
        self = self.with_context(self.create_log('reinstall'))
        self.purge_links()
        self.purge()
        self.deploy()
        self.deploy_links()
        self.end_log()

    @api.model
    def create(self, vals):
        """
        Override the default create function to create log, call deploy hook,
        and call unlink if something went wrong.

        :param vals: The values needed to create the record.
        """
        res = super(ExchangeModel, self).create(vals)
        res = res.with_context(res.create_log('create'))
        try:
            res.deploy()
            res.deploy_links()
        except:
            res.log('===================')
            res.log('FAIL! Reverting...')
            res.log('===================')
            res = res.with_context(nosave=True)
            res.unlink()
            raise
        res.end_log()
        return res

    @api.one
    def unlink(self):
        """
        Override the default unlink function to create log and call purge hook.
        """
        try:
            self.purge_links()
            self.purge()
        except:
            pass
        res = super(ExchangeModel, self).unlink()
        # Security to prevent log to write in a removed exchange.log
        if 'logs' in self.env.context \
                and self._name in self.env.context['logs'] \
                and self.id in self.env.context['logs'][self._name]:
            del self.env.context['logs'][self._name][self.id]
        log_ids = self.env['exchange.log'].search(
            [('model', '=', self._name), ('res_id', '=', self.id)])
        log_ids.unlink()
        return res

    @api.multi
    def execute_local(self, cmd, path=False, shell=False):
        """
        Method which can be used to execute command on the local system.

        :param cmd: The command we need to execute.
        :param path: The path where the command shall be executed.
        :param shell: Specify if the command shall be executed in shell mode.
        """
        self.log('command : ' + ' '.join(cmd))
        cwd = os.getcwd()
        if path:
            self.log('path : ' + path)
            os.chdir(path)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, shell=shell)
        out = ''
        for line in proc.stdout:
            out += line
            line = 'stdout : ' + line
            self.log(line)
        os.chdir(cwd)
        return out

    @api.multi
    def local_file_exist(self, localfile):
        """
        Method which check is a file exist on the local system.

        :param localfile: The path to the file we need to check.
        """
        return os.path.isfile(localfile)

    @api.multi
    def local_dir_exist(self, localdir):
        """
        Method which check is a directory exist on the local system.

        :param localdir: The path to the dir we need to check.
        """
        return os.path.isdir(localdir)

    @api.multi
    def execute_write_file(self, localfile, value):
        """
        Method which write in a file on the local system.

        :param localfile: The path to the file we need to write.
        :param value: The value we need to write in the file.
        """
        f = open(localfile, 'a')
        f.write(value)
        f.close()

    @api.multi
    def generate_random_password(size):
        """
        Method which can be used to generate a random password.

        :param size: The size of the random string we need to generate.
        """
        return ''.join(
        random.choice(string.ascii_uppercase + string.ascii_lowercase
                      + string.digits)
        for _ in range(size))

    @api.multi
    def _create_key(self):
        """
        Generate a key on the filesystem.
        """
        if not self.env.ref('exchange.config.settings').code:
            raise except_orm(
                _('Data error!'),
                _("You need to specify the sysadmin email in configuration"))

        self.execute_local(['mkdir', '/tmp/key_' + self.env.uid])
        self.execute_local(['ssh-keygen', '-t', 'rsa', '-C',
                            self.email_sysadmin, '-f',
                            '/tmp/key_' + self.env.uid + '/key', '-N', ''])
        return True