from content_apis.helpers import response_object_or_error

class Bucket:
    def __init__(self, conn, name):
        self.conn = conn
        self.name = name

    @classmethod
    def create(cls, conn, name, region, immutable, version, lock):
        resp = conn.http_post(
            f"{conn.url}/api/buckets/",
            {
                "name" : name,
                "region": "in-blr",
                "immutable": immutable,
                "version": version,
                "lock": lock
            }
        )
        return response_object_or_error("Bucket", resp, 201)

    # def update(self):
    #     ...

    # def delete(self):
    #     ...

    # def list_cnames(self):
    #     ...

    # def create_object(self, ..):
    #     Document.create(self, ...)

    # def objects(self, path):
    #     Document(self.conn, self.bucket_name, path)