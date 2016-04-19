# -*- coding: utf-8 -*-
# © <2016> <Moneygrid Project, Lucas Huber
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
# TODO, This functions are mostly not yet needed, Deleting the unused ones is a final task
from openerp import models, fields, api, _
from openerp.exceptions import except_orm
from datetime import datetime, timedelta
import subprocess
import os.path
import string
import random
from os.path import expanduser
# import json
# import logging
# import werkzeug
# from hashlib import sha256
import uuid
import hashlib


class ExchangeBaseModel(models.AbstractModel):
    """
    Define the exchange.model abstract object, which is inherited by most
    objects in exchange.
    """

    _name = 'exchange.model'
    _autodeploy = True

    @property
    def hash_password(self, password):
        """
        Property returning a hashed and salted password
        (uuid is used to generate a random number)
        """
        salt = uuid.uuid4().hex
        return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

    @property
    def check_password(self, hashed_password, user_password):
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

    @property
    def hash_string(self, text):
        """
        Property returning a hash of a string
        """
        return hashlib.sha256(text.encode()).hexdigest()

    """
    new_pass = raw_input('Please enter a password: ')
    hashed_password = hash_password(new_pass)
    print('The string to store in the db is: ' + hashed_password)
    old_pass = raw_input('Now please enter the password again to check: ')
    if check_password(hashed_password, old_pass):
        print('You entered the right password')
    else:
        print('I am sorry but the password does not match')
    """

    @property
    def email_sysadmin(self):
        """
        Property returning the sysadmin email of the exchange.
        """
        return self.env.ref('exchange.config.settings').email_sysadmin

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
        if not self.env.ref('exchange.config.settings').email_sysadmin:
            raise except_orm(
                _('Data error!'),
                _("You need to specify the sysadmin email in configuration"))

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



