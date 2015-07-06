# #######
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
from cloudify import ctx
from cloudify.decorators import operation

from gcp.gcp import GoogleCloudPlatform
from gcp.compute import constants
from gcp.compute import utils
from gcp.storage import Object


class Image(GoogleCloudPlatform):
    def __init__(self,
                 config,
                 logger,
                 name,
                 url=None,
                 id=None):
        """
        Create Image object

        :param config:
        :param logger:
        :param url: path to image to be uploaded
        :param id: image_id
        """
        super(Image, self).__init__(config, logger, name)
        self.url = url
        self.id = id
        self.config = config

    def create(self):
        # upload tar.gz to a bucket
        # check if this bucket exists, create if not
        # bucket will be named by project name
        # insert image from tar.gz to the projects

        self.discovery.images().insert(
            project=self.project,
            body=self.to_dict()).execute()

    def upload_and_create(self, file_path):
        obj = Object(self.config, self.logger, self.name)
        self.url = obj.upload_to_bucket(path=file_path)
        self.create()

    def delete(self):
        return self.discovery.images().delete(project=self.project,
                                              name=self.name).execute()

    def list_objects(self):
        storage = self.create_discovery(discovery=constants.STORAGE_DISCOVERY,
                                        scope=constants.STORAGE_SCOPE_RW)
        response = storage.objects().list(bucket=self.project).execute()
        return response.get('items')

    def to_dict(self):
        body = {
            'name': self.name,
            'rawDisk': {
                'source': self.url,
                'containerType': 'TAR'
            }
        }
        return body


@operation
@utils.throw_cloudify_exceptions
def create(gcp_config, image_name, image_path, **kwargs):
    image = Image(gcp_config, ctx.logger, image_name)
    local_path = ctx.download_resource(image_path)
    image.upload_and_create(local_path)
    ctx.instance.runtime_properties[constants.NAME] = image.name


@operation
@utils.throw_cloudify_exceptions
def delete(gcp_config, **kwargs):
    name = ctx.instance.runtime_properties.pop(constants.NAME, None)
    image = Image(gcp_config, ctx.logger, name)
    image.delete()
