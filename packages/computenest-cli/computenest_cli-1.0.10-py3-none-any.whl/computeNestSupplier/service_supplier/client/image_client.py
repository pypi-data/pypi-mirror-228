# -*- coding: utf-8 -*-
import json
from computeNestSupplier.service_supplier.client.oos_client import OosClient
from alibabacloud_oos20190601 import models as oos_20190601_models


class ImageClient(OosClient):
    ACS_ECS_UPDATE_IMAGE = 'ACS-ECS-UpdateImage'

    def __init__(self, region_id, access_key_id, access_key_secret):
        super().__init__(region_id, access_key_id, access_key_secret)
        self.client = self.create_client_oos()

    def start_update_Image_execution(self, image_data):
        json_data = json.dumps(image_data)
        start_execution_request = oos_20190601_models.StartExecutionRequest(
            region_id=self.region_id,
            template_name=self.ACS_ECS_UPDATE_IMAGE,
            parameters=json_data
        )
        response = self.client.start_execution(start_execution_request)
        execution_id = response.body.execution.execution_id
        return execution_id

    def list_execution(self, execution_id):
        list_execution_request = oos_20190601_models.ListExecutionsRequest(execution_id=execution_id)
        response = self.client.list_executions(list_execution_request)
        return response
