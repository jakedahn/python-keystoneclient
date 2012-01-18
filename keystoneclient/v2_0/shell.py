# Copyright 2010 Jacob Kaplan-Moss
# Copyright 2011 OpenStack LLC.
# Copyright 2011 Nebula, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from keystoneclient.v2_0 import client
from keystoneclient import utils

CLIENT_CLASS = client.Client


def do_user_list(kc, args):
    users = kc.users.list(tenant_id=args.tenant_id)
    utils.print_list(users, ['id', 'enabled', 'email', 'name', 'tenantId'])


# TODO this is broken
@utils.arg('username', metavar='<username>', nargs='?')
@utils.arg('password', metavar='<password>', nargs='?')
@utils.arg('email', metavar='<email>', nargs='?')
@utils.arg('default_tenant', metavar='<default_tenant', nargs='?')
@utils.arg('enabled', metavar='<enabled', nargs='?', default=True)
def do_user_create(kc, args):
    user = kc.users.create(args.name, args.password, args.email,
                           tenant_id=args.default_tenant, enabled=args.enabled)

    print "###", user, "###"
    print "===", args.__dict__, "###"

def do():
    """docstring for do"""
    pass