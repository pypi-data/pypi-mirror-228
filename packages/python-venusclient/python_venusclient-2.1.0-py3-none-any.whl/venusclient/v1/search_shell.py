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


def do_get_log(cs, args):
    """get log content"""
    endpoint = cs.search.get_log(args)
    print(endpoint)
    return endpoint


def do_get_type_host(cs, args):
    """get host name all cluster"""
    endpoint = cs.search.get_type_host(args)
    print(endpoint)
    return endpoint


def do_get_type_level(cs, args):
    """get log level all cluster"""
    endpoint = cs.search.get_type_host(args)
    print(endpoint)
    return endpoint


def do_get_type_module(cs, args):
    """get log module all cluster"""
    endpoint = cs.search.get_type_module(args)
    print(endpoint)
    return endpoint


def do_get_type_program(cs, args):
    """get log module all cluster"""
    endpoint = cs.search.get_type_program(args)
    print(endpoint)
    return endpoint


def do_get_instance_request_ids(cs, args):
    """get instance request id list."""
    endpoint = cs.search.get_instance_request_ids(args)
    print(endpoint)
    return endpoint


def do_get_analyse_logs(cs, args):
    """get search analyse logs"""
    endpoint = cs.search.do_get_analyse_logs(args)
    print(endpoint)
    return endpoint
