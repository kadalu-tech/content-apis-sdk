# noqa # pylint: disable=missing-module-docstring
from content_apis.regions import Region
from content_apis.buckets import Bucket
from content_apis.objects import Document
from content_apis.helpers import ConnectionBase, APIError, json_from_response

class Connection(ConnectionBase):
    def __init__(self, url, username=None, password=None, user_id=None, token=None):
        """Intialise Connection and Login to Kadalu Content API"""
        self.url = url.strip("/")
        super().__init__()

        if username is not None and password is not None:
            resp = self.http_post(self.url + "/api/api-keys", {"username": username, "password": password})

            # TODO: Send correct error response from API when username/password/etc are wrong
            # Currently response data seems to be empty.
            # if resp.status != 201:
            #     raise APIError(resp)

            resp_json = json_from_response(resp)

            self.user_id = resp_json["user_id"]
            self.token = resp_json["token"]

        if user_id is not None and token is not None:
            self.user_id = user_id
            self.token = token


    def create_region(self, name, address):
        """ Create a new region """
        return Region.create(self, name, address)


    def create_bucket(self, name, region="", immutable=False, version=False, lock=False):
        """ Create a new bucket """
        return Bucket.create(self, name, region, immutable, version, lock)


    def list_buckets(self):
        """ Return list of buckets """
        return Bucket.list_buckets(self)


    def bucket(self, name=None):
        return Bucket(self, name)


    def create_object(self, path, data, object_type):
        """ Create default("/") object """
        return Document.create(self, "/", path, data, object_type)


    def list_objects(self):
        """ List all default("/") objects """
        return Document.list(self, "/")
