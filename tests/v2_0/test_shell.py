import os
import mock
import httplib2
import json
import urlparse

from keystoneclient import client as kc
from keystoneclient import shell as openstack_shell
from keystoneclient import exceptions
from tests import utils


class ShellTest(utils.TestCase):

    # Patch os.environ to avoid required auth info.
    def setUp(self):
        super(ShellTest, self).setUp()
        self.TEST_REQUEST_HEADERS = {'X-Auth-Token': 'aToken',
                                     'User-Agent': 'python-keystoneclient'}
        self.TEST_POST_HEADERS = {'Content-Type': 'application/json',
                                  'X-Auth-Token': 'aToken',
                                  'User-Agent': 'python-keystoneclient'}
        self.TEST_USERS = {
                            "users": {
                                "values": [
                                    {
                                        "email": "None",
                                        "enabled": True,
                                        "id": 1,
                                        "name": "admin"
                                    },
                                    {
                                        "email": "None",
                                        "enabled": True,
                                        "id": 2,
                                        "name": "demo"
                                    },
                                ]
                            }
                        }
        
        global _old_env
        fake_env = {
            'OS_USERNAME': 'username',
            'OS_PASSWORD': 'password',
            'OS_TENANT_ID': 'tenant_id',
            'OS_AUTH_URL': 'http://nova:5000/v2.0',
        }
        _old_env, os.environ = os.environ, fake_env.copy()

        # Make a fake shell object, a helping wrapper to call it, and a quick
        # way of asserting that certain API calls were made.
        global shell, _shell, assert_called, assert_called_anytime
        _shell = openstack_shell.OpenStackIdentityShell()
        shell = lambda cmd: _shell.main(cmd.split())

    def tearDown(self):
        global _old_env
        os.environ = _old_env

    def test_user_list(self):
        kc = self.client
        kc.users = self.mox.CreateMockAnything()
        kc.users.list(tenant_id=None).AndReturn(self.TEST_USERS)
        
        kc.authenticate = self.mox.CreateMockAnything()
        kc.authenticate().AndReturn(True)
        
        self.mox.ReplayAll()

        shell('user-list')
        # [self.assertTrue(isinstance(u, users.User)) for u in user_list]

