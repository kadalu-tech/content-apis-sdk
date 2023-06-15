from content_apis.helpers import response_object_or_error
from content_apis.objects import Document

class Bucket:
    def __init__(self, conn, name):
        self.conn = conn
        self.name = name

    @classmethod
    def create(cls, conn, name, region, immutable, version, lock):
        # TODO: Handle Invalid Region Name, when only name is passed.
        # (Had removed buckets table / delete from buckets;)

        print("name", name)
        print("region", region)

        resp = conn.http_post(
            f"{conn.url}/api/buckets/",
            {
                "name" : name,
                "region": region,
                "immutable": immutable,
                "version": version,
                "lock": lock
            }
        )
        return response_object_or_error("Bucket", resp, 201)

    @classmethod
    def list_buckets(cls, conn):
        resp = conn.http_get(
            f"{conn.url}/api/buckets"
        )
        return response_object_or_error("Bucket", resp, 200)

    def get(self):
        resp = self.conn.http_get(
            f"{self.conn.url}/api/buckets/{self.name}"
        )
        return response_object_or_error("Bucket", resp, 200)

    def update(self, name=None, region=None, immutable=None, version=None, lock=None):

        print("name", name, "region", region)
        resp = self.conn.http_put(
            f"{self.conn.url}/api/buckets/{self.name}",
            {
                "name": name,
                "region": region,
                "immutable": immutable,
                "version": version,
                "lock": lock
            }
        )

        # Update object name so deletion can be done from the same object after updation.
        if resp.status == 200 and name is not None:
            self.name = name

        return response_object_or_error("Bucket", resp, 200)


    def delete(self):
        resp = self.conn.http_delete(f"{self.conn.url}/api/buckets/{self.name}")
        return response_object_or_error("Bucket", resp, 204)


    # def create_cname(self):
    #     ...

    # def create_share(self):
    #     ...

    # def share(self):
    #     ...

    # def cname(self):
    #     ...

    # def list_shares(self):
    #     ...

    # def list_cnames(self):
    #     ...

    def create_object(self, path, data, object_type):
        Document.create(self.conn, self.name, path, data, object_type)

    def object(self, path):
        return Document(self.conn, self.name, path)
