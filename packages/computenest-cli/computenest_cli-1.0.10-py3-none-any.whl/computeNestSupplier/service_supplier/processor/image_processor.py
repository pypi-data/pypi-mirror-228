import time
import json
from computeNestSupplier.service_supplier.client.image_client import ImageClient
from computeNestSupplier.service_supplier.common import constant


class ImageProcessor:
    IMAGEID = 'imageId'
    RUNNING = 'Running'
    WAITING = 'Waiting'
    QUEUED = 'Queued'
    FAILED = 'Failed'
    SUCCESS = 'Success'

    def __init__(self, region_id, access_key_id, access_key_secret):
        self.region_id = region_id
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.image = ImageClient(self.region_id, self.access_key_id, self.access_key_secret)

    def process(self, image_data):
        execution_id = self.image.start_update_Image_execution(image_data)
        while True:
            image_data = self.image.list_execution(execution_id)
            status = image_data.body.executions[0].status
            if status == self.RUNNING or status == self.RUNNING or status == self.QUEUED:
                print('Be executing...')
            elif status == self.FAILED:
                print('Execution failed')
                break
            elif status == self.SUCCESS:
                print('Execution successful !')
                break
            time.sleep(100)
        image_data = self.image.list_execution(execution_id)
        outputs = json.loads(image_data.body.executions[0].outputs)
        image_id = outputs[self.IMAGEID]
        return image_id
