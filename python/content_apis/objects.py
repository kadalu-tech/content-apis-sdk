from content_apis.helpers import response_object_or_error

class Document:
    def __init__(self, conn, bucket_name, path):
        self.conn = conn
        self.bucket_name = bucket_name
        self.path = path

    @classmethod
    def create(cls, conn, bucket_name, path, obj_type, data):
        if bucket_name == "/":
            url = f"{conn.url}/api/objects"
        else:
            url = f"{conn.url}/api/buckets/{bucket_name}/objects"

        resp = conn.http_post(
            url,
            {
                "path": path,
                "type": obj_type,
                "data": data
            }
        )
        return response_object_or_error("Object", resp, 201)


    #TODO: Add list of default objects
    @classmethod
    def list(cls, conn, bucket_name):
        resp = conn.http_get(
            f"{conn.url}/api/buckets/{bucket_name}/objects"
        )
        return response_object_or_error("Bucket", resp, 200)


    # TODO: Add default update object
    def get(self):
        resp = self.conn.http_get(
            f"{self.conn.url}/api/buckets/{self.bucket_name}/objects/{self.path}"
        )
        print(resp.status)
        return response_object_or_error("Object", resp, 200)


    # TODO: Check for response once Object Update API is implemented
    # TODO: Add default update object
    def update(self, path=None, data=None, object_type=None):
        resp = self.conn.http_put(
            f"{self.conn.url}/api/buckets/{self.bucket_name}/objects/{self.path}",
            {
                "path": path,
                "data": data,
                "type": object_type
            }
        )

        # Update object name so deletion can be done from the same object after updation.
        if resp.status == 200 and path is not None:
            self.path = path

        return response_object_or_error("Object", resp, 200)


    # TODO: Add default delete object
    def delete(self):
        resp = self.conn.http_delete(f"{self.conn.url}/api/buckets/{self.bucket_name}/objects/{self.path}")
        return response_object_or_error("Object", resp, 204)