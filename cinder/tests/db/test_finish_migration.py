# Copyright 2013 IBM Corp.
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

"""Tests for finish_volume_migration."""


from cinder import context
from cinder import db
from cinder import exception
from cinder import test
from cinder.tests import utils as testutils


class FinishVolumeMigrationTestCase(test.TestCase):
    """Test cases for finish_volume_migration."""

    def setUp(self):
        super(FinishVolumeMigrationTestCase, self).setUp()

    def tearDown(self):
        super(FinishVolumeMigrationTestCase, self).tearDown()

    def test_finish_volume_migration(self):
        ctxt = context.RequestContext(user_id='user_id',
                                      project_id='project_id',
                                      is_admin=True)
        src_volume = testutils.create_volume(ctxt, host='src',
                                             status='migrating')
        dest_volume = testutils.create_volume(ctxt, host='dest',
                                              status='migration_target')
        db.finish_volume_migration(ctxt, src_volume['id'],
                                   dest_volume['id'])

        self.assertRaises(exception.VolumeNotFound, db.volume_get, ctxt,
                          dest_volume['id'])
        src_volume = db.volume_get(ctxt, src_volume['id'])
        self.assertEqual(src_volume['host'], 'dest')
        self.assertEqual(src_volume['status'], 'migrating')
