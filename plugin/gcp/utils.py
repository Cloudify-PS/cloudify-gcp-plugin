########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


def get_item_from_gcp_response(key_field, key_name, items):
    for item in items.get('items', []):
        if item.get(key_field) == key_name:
            return item
    return None


def get_firewall_rule_name(network, firewall):
    return '{0}-{1}'.format(network, firewall['name'])
