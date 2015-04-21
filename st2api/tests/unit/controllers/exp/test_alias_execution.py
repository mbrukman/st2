# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import mock

from st2common.constants.action import LIVEACTION_STATUS_SUCCEEDED
from st2common.services import action as action_service
from st2tests.fixturesloader import FixturesLoader
from tests import FunctionalTest

FIXTURES_PACK = 'aliases'

TEST_MODELS = {
    'actionaliases': ['alias1.yaml', 'alias2.yaml'],
    'actions': ['action1.yaml'],
    'runners': ['runner1.yaml']
}

TEST_LOAD_MODELS = {
    'actionaliases': ['alias3.yaml']
}


class DummyActionExecution(object):
    def __init__(self, id_=None, status=LIVEACTION_STATUS_SUCCEEDED, result=''):
        self.id = id_
        self.status = status
        self.result = result


class TestAliasExecution(FunctionalTest):

    models = None
    alias1 = None
    alias2 = None

    @classmethod
    def setUpClass(cls):
        super(TestAliasExecution, cls).setUpClass()
        cls.models = FixturesLoader().save_fixtures_to_db(fixtures_pack=FIXTURES_PACK,
                                                          fixtures_dict=TEST_MODELS)
        cls.alias1 = cls.models['actionaliases']['alias1.yaml']
        cls.alias2 = cls.models['actionaliases']['alias2.yaml']

    @mock.patch.object(action_service, 'request',
                       return_value=(None, DummyActionExecution(id_=1)))
    def testBasicExecution(self, request):
        alias_execution = 'alias1 Lorem ipsum value1 dolor sit "value2 value3" amet.'
        post_resp = self._do_post(alias_execution)
        self.assertEqual(post_resp.status_int, 200)
        expected_parameters = {'param1': 'value1', 'param2': 'value2 value3'}
        self.assertEquals(request.call_args[0][0].parameters, expected_parameters)

    def _do_post(self, execution, expect_errors=False):
        execution = {'command': execution}
        return self.app.post_json('/exp/aliasexecution', execution,
                                  expect_errors=expect_errors)
