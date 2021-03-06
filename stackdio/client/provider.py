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
from .http import HttpMixin, endpoint, use_admin_auth
from .version import accepted_versions, deprecated


class ProviderMixin(HttpMixin):

    @endpoint("provider_types/")
    def list_provider_types(self):
        """List all providers"""
        return self._get(endpoint, jsonify=True)['results']


    @accepted_versions(">=0.6.1")
    @endpoint("provider_types/")
    def search_provider_types(self, provider_id):
        """List all provider_types"""
        return self._get(endpoint, jsonify=True)['results']


    @deprecated
    @accepted_versions("<0.7")
    @endpoint("provider_types/")
    def get_provider_type_id(self, type_name):
        """Get the id for the provider specified by type_name"""

        result = self._get(endpoint, jsonify=True)
        for provider_type in result['results']:
            if provider_type.get("type_name") == type_name:
                return provider_type.get("id")

        raise StackException("Provider type %s not found" % type_name)


    @use_admin_auth
    @endpoint("providers/")
    def create_provider(self, **kwargs):
        """Create a provider"""

        form_data = {
            "title": None,
            "account_id": None,
            "provider_type": None,
            "access_key_id": None,
            "secret_access_key": None,
            "keypair": None,
            "security_groups": None,
            "route53_domain": None,
            "default_availability_zone": None,
            "private_key": None
        }

        for key in form_data.keys():
            form_data[key] = kwargs.get(key)

        return self._post(endpoint, data=json.dumps(form_data), jsonify=True)


    @endpoint("providers/")
    def list_providers(self):
        """List all providers"""
        return self._get(endpoint, jsonify=True)['results']


    @endpoint("providers/{provider_id}/")
    def get_provider(self, provider_id, none_on_404=False):
        """Return the provider that matches the given id"""
        return self._get(endpoint, jsonify=True, none_on_404=none_on_404)


    @accepted_versions(">=0.6.1")
    @endpoint("providers/")
    def search_providers(self, provider_id):
        """List all providers"""
        return self._get(endpoint, jsonify=True)['results']


    @endpoint("providers/{provider_id}/")
    def delete_provider(self, provider_id):
        """List all providers"""
        return self._delete(endpoint, jsonify=True)['results']


    @deprecated
    @accepted_versions("<0.7")
    def get_provider_id(self, slug, title=False):
        """Get the id for a provider that matches slug. If title is True will
        look at title instead."""

        providers = self.list_providers()

        for provider in providers:
            if provider.get("slug" if not title else "title") == slug:
                return provider.get("id")

        raise StackException("Provider %s not found" % slug)
