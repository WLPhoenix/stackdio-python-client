# -*- coding: utf-8 -*-

# Copyright 2014,  Digital Reasoning
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import json

from .exceptions import StackException
from .http import HttpMixin, endpoint
from .version import accepted_versions, deprecated


class StackMixin(HttpMixin):
    VALID_LOG_TYPES = {
        "provisioning": ['log', 'err'],
        "global-orchestration": ['log', 'err'],
        "orchestration": ['log', 'err'],
        "launch": ['log'],
    }

    @endpoint("stacks/")
    def create_stack(self, stack_data):
        """Launch a stack as described by stack_data"""
        return self._post(endpoint, data=json.dumps(stack_data), jsonify=True)

    @endpoint("stacks/")
    def list_stacks(self):
        """Return a list of all stacks"""
        return self._get(endpoint, jsonify=True)['results']

    @endpoint("stacks/{stack_id}/")
    def get_stack(self, stack_id, none_on_404=False):
        """Get stack info"""
        return self._get(endpoint, jsonify=True, none_on_404=none_on_404)

    @endpoint("stacks/")
    def search_stacks(self, **kwargs):
        """Search for stacks that match the given criteria"""
        return self._get(endpoint, params=kwargs, jsonify=True)['results']

    @endpoint("stacks/{stack_id}/")
    def delete_stack(self, stack_id):
        """Destructively delete a stack forever."""
        return self._delete(endpoint, jsonify=True)

    @endpoint("stacks/{stack_id}/action/")
    def get_valid_stack_actions(self, stack_id):
        return self._get(endpoint, jsonify=True)['available_actions']

    @endpoint("stacks/{stack_id}/action/")
    def do_stack_action(self, stack_id, action):
        """Execute an action on a stack"""
        valid_actions = self.get_valid_stack_actions(stack_id)

        if action not in valid_actions:
            raise StackException("Invalid action, must be one of %s" %
                                 ", ".join(valid_actions))

        data = {"action": action}

        return self._post(endpoint, data=json.dumps(data), jsonify=True)

    @endpoint("stacks/{stack_id}/history/")
    def get_stack_history(self, stack_id):
        """Get stack info"""
        result = self._get(endpoint, none_on_404=True, jsonify=True)
        if result is None:
            raise StackException("Stack %s not found" % stack_id)
        else:
            return result

    @deprecated
    @accepted_versions("<0.7")
    def get_stack_id(self, title):
        """Find a stack id"""

        stacks = self.list_stacks()
        for stack in stacks:
            if stack.get("title") == title:
                return stack.get("id")

        raise StackException("Stack %s not found" % title)

    @endpoint("stacks/{stack_id}/hosts/")
    def get_stack_hosts(self, stack_id):
        """Get a list of all stack hosts"""
        return self._get(endpoint, jsonify=True)['results']

    @endpoint("stacks/{stack_id}/hosts/")
    def describe_hosts(self, stack_id, key="fqdn", ec2=False):
        """Retrieve a list of info about a stack. Defaults to the id for each
        host, but you can specify any available key. Setting ec2=True will
        force it to inspect the ec2_metadata field."""

        EC2 = "ec2_metadata"
        result = self._get(endpoint, jsonify=True)

        stack_details = []

        for host in result['results']:
            if not ec2:
                host_details = host.get(key)
            else:
                host_details = host.get(EC2).get(key)

            if host_details is not None:
                stack_details.append(host_details)

        if stack_details:
            return stack_details

        raise StackException("Key %s for stack %s not available" % (key, stack_id))

    @endpoint("stacks/{stack_id}/logs/{log_type}.{level}.{date}")
    def get_logs(self, stack_id, log_type, level='log', date='latest', tail=None):
        """Get logs for a stack"""

        if log_type and log_type not in self.VALID_LOG_TYPES:
            raise StackException("Invalid log type, must be one of %s" %
                                 ", ".join(self.VALID_LOG_TYPES.keys()))

        if level not in self.VALID_LOG_TYPES[log_type]:
            raise StackException("Invalid log level, must be one of %s" %
                                 ", ".join(self.VALID_LOG_TYPES[log_type]))

        return self._get(endpoint, params={'tail': tail}).text

    @endpoint("stacks/{stack_id}/security_groups/")
    def list_access_rules(self, stack_id):
        """Get Access rules for a stack"""

        return self._get(endpoint, jsonify=True)['results']

    @deprecated
    @accepted_versions("<0.7")
    def get_access_rule_id(self, stack_id, title):
        """Find an access rule id"""

        rules = self.list_access_rules(stack_id)

        try:
            for group in rules:
                if group.get("blueprint_host_definition").get("title") == title:
                    return group.get("id")
        except TypeError:
            pass

        raise StackException("Access Rule %s not found" % title)

    @endpoint("security_groups/{group_id}/rules/")
    def list_rules_for_group(self, group_id):
        return self._get(endpoint, jsonify=True)

    @endpoint("security_groups/{group_id}/rules/")
    def edit_access_rule(self, group_id, data=None):
        """Add an access rule to a group"""

        return self._put(endpoint, jsonify=True, data=json.dumps(data))
