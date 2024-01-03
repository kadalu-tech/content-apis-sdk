from kadalu_content_apis.helpers import response_object_or_error, Generic
from kadalu_content_apis.objects import Document
from kadalu_content_apis.shares import Share
from kadalu_content_apis.templates import Template

class Folder(Generic):
    def __init__(self, conn=None, name=None, data={}):
        """ Intialise folder """
        super().__init__(data)

        if conn is not None:
            self.conn = conn

        if name is not None:
            self.name = name

    # TODO: Handle Invalid Region Name, when only name is passed.
    @classmethod
    def create(cls, conn, name, region, threads, template):
        """ Create folder """

        resp = conn.http_post(
            f"{conn.url}/api/folders/",
            {
                "name" : name,
                "region": region,
                "threads": threads,
                "template": template
            }
        )
        outdata = response_object_or_error(Folder, resp, 201)
        outdata.conn = conn
        return outdata


    @classmethod
    def list_folders(cls, conn, page, page_size):
        """ List all folders """

        resp = conn.http_get(
            f"{conn.url}/api/folders?page={page}&page_size={page_size}"
        )

        folders = response_object_or_error(Folder, resp, 200)

        def update_conn(folder):
            folder.conn = conn
            return folder

        return list(map(update_conn, folders))

    def get(self):
        """ Return a folder """

        resp = self.conn.http_get(
            f"{self.conn.url}/api/folders/{self.name}"
        )
        outdata = response_object_or_error(Folder, resp, 200)
        outdata.conn = self.conn
        return outdata

    def update(self, name=None, region=None, threads=None, template=None):
        """ Update folders """

        resp = self.conn.http_put(
            f"{self.conn.url}/api/folders/{self.name}",
            {
                "name": name,
                "region": region,
                "threads": threads,
                "template": template
            }
        )

        # Update object name so deletion can be done from the same object after updation.
        if resp.status == 200 and name is not None:
            self.name = name

        outdata = response_object_or_error(Folder, resp, 200)
        outdata.conn = self.conn
        return outdata

    def delete(self, recursive=False):
        """ Delete folders """
        resp = self.conn.http_delete(f"{self.conn.url}/api/folders/{self.name}?recursive={recursive}")
        return response_object_or_error(Folder, resp, 204)

    def create_template(self, name, content, template_type, output_type="text", public=False):
        """ Create template with folder-name """
        return Template.create(self.conn, self.name, name, content, template_type, output_type, public)

    def upload_template(self, file_path, template_type, name="", output_type="text", public=False):
        """ Upload Template with-folder-name"""
        return Template.upload_create(self.conn, self.name, file_path, template_type, name, output_type, public)

    def list_templates(self, page=1, page_size=30):
        """ List all templates with folder-name"""
        return Template.list_templates(self.conn, self.name, page, page_size)

    def template(self, name):
        """ Return Template instance with folder-name"""
        return Template(self.conn, self.name, name)

    def create_object(self, path, data, object_type, threads=False, template=None):
        """ Create object with folder-name """
        return Document.create(self.conn, self.name, path, data, object_type, threads, template)


    def upload_object(self, file_path, object_type, path="", threads=False, template=None):
        """ Create default("/") object """
        return Document.upload_create(self.conn, self.name, file_path, object_type, path, threads, template)


    def list_objects(self, page=1, page_size=30):
        """ List objects with folder-name """
        return Document.list(self.conn, self.name, page, page_size)


    def object(self, path):
        """ Return Object/Document instance """
        return Document(self.conn, self.name, path)


    def create_share(self, public=False, use_long_url=False, password="", use_token=False, disable=False, revoke=False, expire=False, role=""):
        """ Create Share with folder name """
        return Share.create(self.conn, self.name, "", public, use_long_url, password, use_token, disable, revoke, expire, role)


    def list_shares(self, page=1, page_size=30):
        """ List all Shares within a folder """
        return Share.list(self.conn, self.name, "", page, page_size)


    def share(self, share_id):
        """ Return a Share instance """
        return Share(self.conn, self.name, "", share_id)


    # def create_cname(self):
    #     ...

    # def cname(self):
    #     ...

    # def list_cnames(self):
    #     ...
