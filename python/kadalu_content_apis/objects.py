import os
import json

from kadalu_content_apis.shares import Share
from kadalu_content_apis.helpers import response_object_or_error, APIError, Generic

class Document(Generic):
    def __init__(self, conn=None, folder_name=None, path=None, data={}):
        """ Intialise Document/Object """
        super().__init__(data)

        if conn is not None:
            self.conn = conn

        if folder_name is not None:
            self.folder_name = folder_name

        if path is not None:
            self.path = path


    @classmethod
    def create(cls, conn, folder_name, path, data, object_type, threads, template):
        """ Create object of both 'default' folder and with folder-name """

        folder_name = folder_name.lstrip("/")
        url = f"{conn.url}/api/objects/{folder_name}"
        resp = conn.http_post(
            url,
            {
                "path": path,
                "type": object_type,
                "data": data,
                "threads": threads,
                "template": template
            }
        )
        outdata = response_object_or_error(Document, resp, 201)
        outdata.conn = conn
        outdata.folder_name = folder_name
        return outdata

    @classmethod
    def upload_create(cls, conn, folder_name, file_path, object_type, path, threads, template):
        """ Upload object data at file_path """

        file_content = ""

        folder_name = folder_name.lstrip("/")
        url = f"{conn.url}/api/objects/{folder_name}"

        with open(file_path, 'rb') as file:
            file_content = file.read()

        # If path is empty, set filepath as path excluding the relative path
        if path == "":
            path = os.path.basename(file_path)

        data = {
            "path": path,
            "type": object_type,
            "threads": json.dumps(threads),
            "template": template
        }

        files = {
            "data": (file_path, file_content)
        }

        resp = conn.http_post_upload(url, data, files)
        outdata = response_object_or_error(Document, resp, 201)
        outdata.conn = conn
        outdata.folder_name = folder_name
        return outdata

    def upload(self, file_path, object_type=None, path=None, template=None):
        """ Upload object data at file_path """

        file_content = ""

        folder_name = self.folder_name.lstrip("/")
        url = f"{conn.url}/api/objects/{folder_name}"

        with open(file_path, 'rb') as file:
            file_content = file.read()

        data = {}
        if path is not None:
            data["path"] = path

        if object_type is not None:
            data["type"] = object_type

        if template is not None:
            data["template"] = template

        files = {
            "data": (file_path, file_content)
        }

        resp = self.conn.http_put_upload(url, data, files)
        outdata = response_object_or_error(Document, resp, 200)
        outdata.conn = self.conn
        outdata.folder_name = folder_name
        return outdata

    @classmethod
    def list(cls, conn, folder_name, page, page_size):
        """ List object(s) of both default("/") and with folder-name """

        folder_name = folder_name.lstrip("/")
        url = f"{conn.url}/api/objects/{folder_name}?page={page}&page_size={page_size}"

        resp = conn.http_get(url)
        objects = response_object_or_error(Document, resp, 200)

        def update_conn(obj):
            obj.conn = conn
            obj.folder_name = folder_name
            return obj

        return list(map(update_conn, objects))


    # TODO: Handle empty responses
    # Ex: Pass non-existent object_name under root(/). Status Code = 200, But resp.data is empty
    def get(self):
        """ Return object of both default("/") and with folder-name """

        folder_name = self.folder_name.lstrip("/")
        print(self.path)
        url = f"{self.conn.url}/api/objects/{folder_name}/{self.path}"

        resp = self.conn.http_get(url)

        outdata = response_object_or_error(Document, resp, 200)
        outdata.conn = self.conn
        outdata.folder_name = self.folder_name
        return outdata


    # TODO: Check for response once Object Update API is implemented
    def update(self, path=None, data=None, object_type=None, template=None):
        """ Update object of both default("/") and with folder-name """

        folder_name = self.folder_name.lstrip("/")
        print(self.path)
        url = f"{self.conn.url}/api/objects/{folder_name}/{self.path}"

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
        if resp.status_code == 200 and path is not None:
            self.path = path

        outdata = response_object_or_error(Document, resp, 200)
        outdata.conn = self.conn
        outdata.folder_name = self.folder_name
        return outdata

    def delete(self):
        """ Delete object of both default("/") and with folder-name """

        folder_name = self.folder_name.lstrip("/")
        url = f"{self.conn.url}/api/objects/{folder_name}/{self.path}"
        resp = self.conn.http_delete(url)
        return response_object_or_error(Document, resp, 204)


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
        if resp.status_code != 200:
            raise APIError(resp)
        return str(resp.data, 'utf-8')


    def create_share(self, public=False, use_long_url=False, password="", use_token=False, disable=False, revoke=False, expire=False, role=""):
        """ Create Share with folder name and object path"""
        return Share.create(self.conn, self.folder_name, self.path, public, use_long_url, password, use_token, disable, revoke, expire, role)


    def list_shares(self, page=1, page_size=30):
        """ List all Shares within a folder """
        return Share.list(self.conn, self.folder_name, self.path, page, page_size)


    def share(self, share_id):
        """ Return a Share instance """
        return Share(self.conn, self.folder_name, self.path, share_id)


class DocumentThread(Generic):
    def __init__(self, conn=None, thread_id=None, data={}):
        """ Intialise DocumentThread/Object """
        super().__init__(data)
        if conn is not None:
            self.conn = conn
        if thread_id is not None:
            self.thread_id = thread_id

    def update(self, thread_type=None, meta=None, data=None):
        url = f"{self.conn.url}/api/threads/{self.thread_id}"

        resp = self.conn.http_put(
            url,
            {
                "data": data,
                "meta": meta,
                "type": thread_type
            }
        )
        outdata = response_object_or_error(DocumentThread, resp, 200)
        outdata.conn = self.conn
        return outdata

    def delete(self):
        url = f"{self.conn.url}/api/threads/{self.thread_id}"
        resp = self.conn.http_delete(url)
        return response_object_or_error(DocumentThread, resp, 204)
