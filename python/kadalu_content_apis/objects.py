import os
from kadalu_content_apis.shares import Share
from kadalu_content_apis.helpers import response_object_or_error, APIError

class Document:
    def __init__(self, conn, folder_name, path):
        """ Intialise Document/Object """
        self.conn = conn
        self.folder_name = folder_name
        self.path = path


    @classmethod
    def create(cls, conn, folder_name, path, data, object_type, immutable, version, lock, template):
        """ Create object of both default("/") and with folder-name """

        folder_name = folder_name.lstrip("/")
        if folder_name == "":
            url = f"{conn.url}/api/objects"
        else:
            url = f"{conn.url}/api/folders/{folder_name}/objects"
        resp = conn.http_post_upload(
            url,
            {
                "path": path,
                "type": object_type,
                "data": data,
                "immutable": immutable,
                "version": version,
                "lock": lock,
                "template": template
            }
        )
        return response_object_or_error("Object", resp, 201)


    @classmethod
    def upload(cls, conn, folder_name, file_path, object_type, path, immutable, version, lock, template):
        """ Upload object data at file_path """

        file_content = ""

        folder_name = folder_name.lstrip("/")
        if folder_name == "":
            url = f"{conn.url}/api/objects"
        else:
            url = f"{conn.url}/api/folders/{folder_name}/objects"

        with open(file_path, "r") as file:
            file_content = file.read()

        # If path is empty, set filepath as path excluding the relative path
        if path == "":
            path = os.path.basename(file_path)

        meta = {
                "path": path,
                "type": object_type,
                "immutable": immutable,
                "version": version,
                "lock": lock,
                "template": template
        }

        resp = conn.http_post_upload(
            url,
            meta, file_path, file_content
        )
        return response_object_or_error("Object", resp, 201)


    @classmethod
    def list(cls, conn, folder_name):
        """ List object(s) of both default("/") and with folder-name """

        folder_name = folder_name.lstrip("/")
        if folder_name == "":
            url = f"{conn.url}/api/objects"
        else:
            url = f"{conn.url}/api/folders/{folder_name}/objects"

        resp = conn.http_get(url)
        return response_object_or_error("folder", resp, 200)


    # TODO: Handle empty responses
    # Ex: Pass non-existent object_name under root(/). Status Code = 200, But resp.data is empty
    def get(self):
        """ Return object of both default("/") and with folder-name """

        folder_name = self.folder_name.lstrip("/")
        if folder_name == "":
            url = f"{self.conn.url}/api/objects/{self.path}"
        else:
            url = f"{self.conn.url}/api/folders/{folder_name}/objects/{self.path}"

        resp = self.conn.http_get(url)
        return response_object_or_error("Object", resp, 200)


    # TODO: Check for response once Object Update API is implemented
    def update(self, path=None, data=None, object_type=None, template=None):
        """ Update object of both default("/") and with folder-name """

        folder_name = self.folder_name.lstrip("/")
        if folder_name == "":
            url = f"{self.conn.url}/api/objects"
        else:
            url = f"{self.conn.url}/api/folders/{folder_name}/objects/{self.path}"

        resp = self.conn.http_put(
            url,
            {
                "path": path,
                "data": data,
                "type": object_type,
                "template": template
            }
        )

        # Update object name so deletion can be done from the same object after updation.
        if resp.status == 200 and path is not None:
            self.path = path

        return response_object_or_error("Object", resp, 200)


    def delete(self):
        """ Delete object of both default("/") and with folder-name """

        folder_name = self.folder_name.lstrip("/")
        if self.folder_name == "":
            url = f"{self.conn.url}/api/objects/{self.path}"
        else:
            url = f"{self.conn.url}/api/folders/{folder_name}/objects/{self.path}"
        resp = self.conn.http_delete(url)
        return response_object_or_error("Object", resp, 204)


    def get_rendered(self, template=""):
        """ Return rendered of both default("/") and with folder-name """

        folder_name = self.folder_name.lstrip("/")
        if folder_name == "":
            url = f"{self.conn.url}/api/content/objects/{self.path}"
        else:
            url = f"{self.conn.url}/api/content/folders/{folder_name}/objects/{self.path}"

        resp = self.conn.http_get(url)

        # TODO: Send response in correct way
        # return response_object_or_error("Object", resp, 200)
        if resp.status != 200:
            raise APIError(resp)
        return str(resp.data, 'utf-8')


    def create_share(self, public=False, use_long_url=False, password="", use_token=False, role=""):
        """ Create Share with folder name and object path"""
        return Share.create(self.conn, self.folder_name, self.path, public, use_long_url, password, use_token, role)


    def list_shares(self):
        """ List all Shares within a folder """
        return Share.list(self.conn, self.folder_name, self.path)


    def share(self, share_id):
        """ Return a Share instance """
        return Share(self.conn, self.folder_name, self.path, share_id)
