import time
import json
import os
import re


from Tea.exceptions import TeaException
from computeNestSupplier.service_supplier.client.artifact_client import ArtifactClient
from computeNestSupplier.service_supplier.common.file import File
from computeNestSupplier.service_supplier.common.credentials import Credentials
from computeNestSupplier.service_supplier.common.util import Util
from computeNestSupplier.service_supplier.processor.image_processor import ImageProcessor
from computeNestSupplier.service_supplier.common import constant


class ArtifactProcessor:
    DATA = 'data'
    RESULT = 'result'
    IMAGE_BUILDER = 'ImageBuilder'
    ARTIFACT = 'artifact'
    DRAFT = 'draft'
    COMMAND_CONTENT = 'CommandContent'
    ENTITY_ALREADY_EXIST_DRAFT_ARTIFACT = 'EntityAlreadyExist.DraftArtifact'

    def __init__(self, region_id, access_key_id, access_key_secret):
        self.region_id = region_id
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.artifact = ArtifactClient(self.region_id, self.access_key_id, self.access_key_secret)

    def __get_file_artifact_url(self, artifact_name):
        get_artifact_data = json.loads(self.artifact.get_artifact(artifact_name).body.artifact_property)
        url = get_artifact_data.get(constant.URL)
        return url

    def __create_image_from_image_builder(self, data, artifact_data):
        data_image = data.get(self.IMAGE_BUILDER)
        id_image = artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.IMAGE_ID)
        id_image_match = Util.regular_expression(id_image)
        data_image_oos = data_image.get(id_image_match[1])
        command_content = data_image_oos[self.COMMAND_CONTENT]
        # 识别命令语句中的占位符
        pattern = r'\$\{Artifact\.(.*?)\.ArtifactProperty\.Url\}'
        matches = re.findall(pattern, command_content)
        if matches:
            artifact_key = matches[0].strip()
            artifact_name = data[constant.ARTIFACT].get(artifact_key, {}).get(constant.ARTIFACT_NAME)
            url = self.__get_file_artifact_url(artifact_name)
            parts = url.split("/")
            # 截取文件部署物下载链接的后半部分
            artifact_url = parts[-2] + "/" + parts[-1]
            placeholder = f'${{Artifact.{artifact_key}.ArtifactProperty.Url}}'
            # 替换真正的url
            command_content = command_content.replace(placeholder, artifact_url)
            data_image_oos[self.COMMAND_CONTENT] = command_content
        data_image_oos = Util.lowercase_first_letter(data_image_oos)
        image_processor = ImageProcessor(self.region_id, self.access_key_id, self.access_key_secret)
        return image_processor.process(data_image_oos)

    def __replace_artifact_file_path_with_url(self, file_path):
        credentials = Credentials(self.region_id, self.access_key_id, self.access_key_secret)
        file = File(self.region_id, self.access_key_id, self.access_key_secret)
        data = credentials.get_artifact_repository_credentials(constant.FILE)
        file_artifact_url = file.put_file(data, file_path, self.ARTIFACT)
        return file_artifact_url

    def __relsase_artifact(self, artifact_id, artifact_name):
        self.artifact.release_artifact(artifact_id)
        while True:
            # 定时检测部署物发布状态
            data_response = self.artifact.list_artifact(artifact_name)
            artifact_version = data_response.body.artifacts[0].max_version
            if artifact_version == self.DRAFT:
                print('The artifact is being released...')
            else:
                print('The release is complete')
            time.sleep(10)
            if artifact_version != self.DRAFT:
                break

    def process(self, data_config, file_path_config):
        data_artifact = data_config.get(constant.ARTIFACT)
        file = File(self.region_id, self.access_key_id, self.access_key_secret)
        for artifact_data in data_artifact.values():
            if constant.ARTIFACT_NAME in artifact_data:
                artifact_type = artifact_data.get(constant.ARTIFACT_TYPE)
                artifact_name = artifact_data.get(constant.ARTIFACT_NAME)
                artifact_data_list = self.artifact.list_artifact(artifact_name)
                if len(artifact_data_list.body.artifacts) == 0:
                    if artifact_type == constant.FILE:
                        # 将相对路径替换成绝对路径
                        file_path = os.path.join(os.path.dirname(file_path_config),
                                                 artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.URL))
                        # 将文件部署物的本地路径替换成Url
                        artifact_data[constant.ARTIFACT_PROPERTY][constant.URL] = self.__replace_artifact_file_path_with_url(file_path)
                    elif artifact_type == constant.ECS_IMAGE:
                        if self.IMAGE_BUILDER in data_config:
                            # 利用oos模版创建镜像
                            artifact_data[constant.ARTIFACT_PROPERTY][constant.IMAGE_ID] = self.__create_image_from_image_builder(data_config, artifact_data)
                    data_create_artifact = self.artifact.create_artifact(artifact_data)
                    artifact_id = data_create_artifact.body.artifact_id
                    print("========================================================")
                    print("The artifact was not found and a new artifact has been created for you")
                    print("The artifact name: ", artifact_name)
                    print("The artifact id: ", artifact_id)
                    print("========================================================")
                    self.__relsase_artifact(artifact_id, artifact_name)
                elif constant.VERSION_NAME not in artifact_data:
                    artifact_id = artifact_data_list.body.artifacts[0].artifact_id
                    print("========================================================")
                    print("No need to update the artifact")
                    print("The artifact name: ", artifact_name)
                    print("The artifact id: ", artifact_id)
                    print("========================================================")
                else:
                    if artifact_type == constant.FILE:
                        file_url_existed = self.__get_file_artifact_url(artifact_name)
                        # 将相对路径替换成绝对路径
                        file_path = os.path.join(os.path.dirname(file_path_config),
                                                 artifact_data.get(constant.ARTIFACT_PROPERTY).get(constant.URL))
                        result_artifact = file.check_file_repeat(file_url_existed, file_path)
                        # 检查文件部署物是否重复，重复则不再上传，使用现有Url
                        if result_artifact:
                            artifact_data[constant.ARTIFACT_PROPERTY][constant.URL] = file_url_existed.split('?')[0]
                        else:
                            artifact_data[constant.ARTIFACT_PROPERTY][constant.URL] = self.__replace_artifact_file_path_with_url(file_path)
                    elif artifact_type == constant.ECS_IMAGE:
                        if self.IMAGE_BUILDER in data_config:
                            # 利用oos模版创建镜像
                            artifact_data[constant.ARTIFACT_PROPERTY][constant.IMAGE_ID] = self.__create_image_from_image_builder(data_config, artifact_data)
                    artifact_id = artifact_data_list.body.artifacts[0].artifact_id
                    try:
                        self.artifact.create_artifact(artifact_data, artifact_id)
                    except TeaException as e:
                        if e.code == self.ENTITY_ALREADY_EXIST_DRAFT_ARTIFACT:
                            self.artifact.update_artifact(artifact_data, artifact_id)
                        else:
                            raise
                    print("========================================================")
                    print("Successfully update the artifact!")
                    print("The artifact name: ", artifact_name)
                    print("The artifact id: ", artifact_id)
                    print("========================================================")
                    self.__relsase_artifact(artifact_id, artifact_name)
                data_response = self.artifact.list_artifact(artifact_name)
                artifact_version = data_response.body.artifacts[0].max_version
                artifact_data[constant.ARTIFACT_ID] = artifact_id
                artifact_data[constant.ARTIFACT_VERSION] = artifact_version
        return data_artifact
