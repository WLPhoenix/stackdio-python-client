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
import os

from .http import HttpMixin, endpoint


class SettingsMixin(HttpMixin):

    @endpoint("settings/")
    def set_public_key(self, public_key):
        """Upload a public key for our user. public_key can be the actual key, a
        file handle, or a path to a key file"""

        if isinstance(public_key, file):
            public_key = public_key.read()

        elif isinstance(public_key, str) and os.path.exists(public_key):
            public_key = open(public_key, "r").read()

        data = {
            "public_key": public_key
        }
        return self._put(endpoint, data=json.dumps(data), jsonify=True)
