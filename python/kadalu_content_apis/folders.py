from kadalu_content_apis.helpers import response_object_or_error
from kadalu_content_apis.objects import Document
from kadalu_content_apis.shares import Share

class Folder:
    def __init__(self, conn, name):
        """ Intialise folder """
        self.conn = conn
        self.name = name

    # TODO: Handle Invalid Region Name, when only name is passed.
    @classmethod
    def create(cls, conn, name, region, immutable, version, lock, template):
        """ Create folder """

        resp = conn.http_post(
            f"{conn.url}/api/folders/",
            {
                "name" : name,
                "region": region,
                "immutable": immutable,
                "version": version,
                "lock": lock,
                "template": template
            }
        )
        return response_object_or_error("folder", resp, 201)


    @classmethod
    def list_folders(cls, conn):
        """ List all folders """

        resp = conn.http_get(
            f"{conn.url}/api/folders"
        )
        return response_object_or_error("folder", resp, 200)


    def get(self):
        """ Return a folder """

        resp = self.conn.http_get(
            f"{self.conn.url}/api/folders/{self.name}"
        )
        return response_object_or_error("folder", resp, 200)


    def update(self, name=None, region=None, immutable=None, version=None, lock=None, template=None):
        """ Update folders """

        resp = self.conn.http_put(
            f"{self.conn.url}/api/folders/{self.name}",
            {
                "name": name,
                "region": region,
                "immutable": immutable,
                "version": version,
                "lock": lock,
                "template": template
            }
        )

        # Update object name so deletion can be done from the same object after updation.
        if resp.status == 200 and name is not None:
            self.name = name

        return response_object_or_error("folder", resp, 200)


    def delete(self, recursive=False):
        """ Delete folders """
        resp = self.conn.http_delete(f"{self.conn.url}/api/folders/{self.name}?recursive={recursive}")
        return response_object_or_error("folder", resp, 204)


    def create_object(self, path, data, object_type, immutable=False, version=False, lock=False, template=None):
        """ Create object with folder-name """
        return Document.create(self.conn, self.name, path, data, object_type, immutable, version, lock, template)


    def upload_object(self, file_path, object_type, path="", immutable=False, version=False, lock=False, template=None):
        """ Create default("/") object """
        return Document.upload(self.conn, self.name, file_path, object_type, path, immutable, version, lock, template)


    def list_objects(self):
        """ List objects with folder-name """
        return Document.list(self.conn, self.name)


    def object(self, path):
        """ Return Object/Document instance """
        return Document(self.conn, self.name, path)


    def create_share(self, public=False, use_long_url=False, password="", use_token=False, disable=False, role=""):
        """ Create Share with folder name """
        return Share.create(self.conn, self.name, "", public, use_long_url, password, use_token, disable, role)


    def list_shares(self):
        """ List all Shares within a folder """
        return Share.list(self.conn, self.name, "")


    def share(self, share_id):
        """ Return a Share instance """
        return Share(self.conn, self.name, "", share_id)


    # def create_cname(self):
    #     ...

    # def cname(self):
    #     ...

    # def list_cnames(self):
    #     ...
