# Copyright 2020 Inspur
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from venusclient.common import utils
from venusclient.v1 import basemodels

CREATION_ATTRIBUTES = basemodels.CREATION_ATTRIBUTES


class LogSearch(basemodels.BaseModel):
    model_name = "Searchs"


class SearchManager(basemodels.BaseModelManager):
    api_name = "search"
    base_url = "search"
    resource_class = LogSearch

    def get_log(self, start_time=0, end_time=20, page_size=15,
                page_num=1, module_name='', host_name='', program_name='',
                level=''):
        url = '/v1/search/logs'

        params = {
            'start_time': start_time,
            'end_time': end_time,
            'page_size': page_size,
            'page_num': page_num,
            'module_name': module_name,
            'host_name': host_name,
            'program_name': program_name,
            'level': level
        }
        url += utils.prepare_query_string(params)

        try:
            resp, body = self.api.json_request('GET', url)
            return body
        except Exception as e:
            raise RuntimeError(str(e))

    def get_type_host(self):
        url = '/v1/search/params'

        params = {
            'type': "host_name",
        }
        url += utils.prepare_query_string(params)

        try:
            resp, body = self.api.json_request('GET', url)
            return body
        except Exception as e:
            raise RuntimeError(str(e))

    def get_type_level(self):
        url = '/v1/search/params'

        params = {
            'type': "level",
        }
        url += utils.prepare_query_string(params)

        try:
            resp, body = self.api.json_request('GET', url)
            return body
        except Exception as e:
            raise RuntimeError(str(e))

    def get_type_module(self, args):
        url = '/v1/search/params'

        params = {
            'type': "module_name",
        }
        url += utils.prepare_query_string(params)

        try:
            resp, body = self.api.json_request('GET', url)
            return body
        except Exception as e:
            raise RuntimeError(str(e))

    def get_type_program(self, args):
        url = '/v1/search/params'

        params = {
            'type': "program_name",
        }
        url += utils.prepare_query_string(params)

        try:
            resp, body = self.api.json_request('GET', url)
            return body
        except Exception as e:
            raise RuntimeError(str(e))

    def get_instance_request_ids(self, args):
        url = 'v1/search/instance/request_ids'

        try:
            resp, body = self.api.json_request('GET', url)
            return body
        except Exception as e:
            raise RuntimeError(str(e))

    def do_get_analyse_logs(self, level='', start_time=0, end_time=0,
                            host_name='', module_name='', program_name='',
                            group_name='host_name'):
        url = 'v1/search/analyse/logs'

        params = {
            'group_name': group_name,
            'host_name': host_name,
            'module_name': module_name,
            'program_name': program_name,
            'level': level,
            'start_time': start_time,
            'end_time': end_time
        }
        url += utils.prepare_query_string(params)

        try:
            resp, body = self.api.json_request('GET', url)
            return body
        except Exception as e:
            raise RuntimeError(str(e))
