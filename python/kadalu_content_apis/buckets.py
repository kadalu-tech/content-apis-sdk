from kadalu_content_apis.helpers import response_object_or_error
from kadalu_content_apis.objects import Document

class Bucket:
    def __init__(self, conn, name):
        """ Intialise Bucket """
        self.conn = conn
        self.name = name

    # TODO: Handle Invalid Region Name, when only name is passed.
    @classmethod
    def create(cls, conn, name, region, immutable, version, lock):
        """ Create bucket """

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
        """ List all buckets """

        resp = conn.http_get(
            f"{conn.url}/api/buckets"
        )
        return response_object_or_error("Bucket", resp, 200)


    def get(self):
        """ Return a bucket """

        resp = self.conn.http_get(
            f"{self.conn.url}/api/buckets/{self.name}"
        )
        return response_object_or_error("Bucket", resp, 200)


    def update(self, name=None, region=None, immutable=None, version=None, lock=None):
        """ Update buckets """

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
        """ Delete buckets """
        resp = self.conn.http_delete(f"{self.conn.url}/api/buckets/{self.name}")
        return response_object_or_error("Bucket", resp, 204)


    def create_object(self, path, data, object_type, immutable=False, version=False, lock=False):
        """ Create object with bucket-name """
        return Document.create(self.conn, self.name, path, data, object_type, immutable, version, lock)


    def list_objects(self):
        """ List objects with bucket-name """
        return Document.list(self.conn, self.name)


    def object(self, path):
        """ Return Object/Document instance """
        return Document(self.conn, self.name, path)


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
