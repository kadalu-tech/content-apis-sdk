import json

from kadalu_content_apis.helpers import response_object_or_error, Generic

class Template(Generic):
    def __init__(self, conn=None, folder_name=None, name=None, data={}):
        """ Intialise Template """
        super().__init__(data)

        if conn is not None:
            self.conn = conn

        if folder_name is not None:
            self.folder_name = folder_name

        if name is not None:
            self.name = name

    # TODO: Handle Invalid Region Name, when only name is passed.
    @classmethod
    def create(cls, conn, folder_name, name, content, template_type, output_type, public):
        """ Create template """

        folder_name = folder_name.lstrip("/")
        if folder_name == "":
            url = f"{conn.url}/api/templates"
        else:
            url = f"{conn.url}/api/folders/{folder_name}/templates"

        resp = conn.http_post(
            url,
            {
                "name" : name,
                "content": content,
                "type": template_type,
                "output_type": output_type,
                "public": public

            }
        )
        outdata = response_object_or_error(Template, resp, 201)
        outdata.conn = conn

        return outdata

    @classmethod
    def upload_create(cls, conn, folder_name, file_path, template_type, name, output_type, public):

        folder_name = folder_name.lstrip("/")
        if folder_name == "":
            url = f"{conn.url}/api/templates"
        else:
            url = f"{conn.url}/api/folders/{folder_name}/templates"

        file_content = ""
        with open(file_path, 'rb') as file:
            file_content = file.read()

        # Set name as basename of file_path when name is not passed
        if name == "":
            name = os.path.basename(file_path)

        data = {
            "name" : name,
            "type": template_type,
            "output_type": output_type,
            "public": json.dumps(public)
        }

        files = {
            "content": (file_path, file_content)
        }

        resp = conn.http_post_upload(url, data, files)
        outdata = response_object_or_error(Template, resp, 201)
        outdata.conn = conn

        return outdata

    def upload(self, folder_name, file_path, template_type=None, name=None, output_type=None, public=None):
        folder_name = self.folder_name.lstrip("/")
        if folder_name == "":
            url = f"{self.conn.url}/api/templates/{self.name}"
        else:
            url = f"{self.conn.url}/api/folders/{self.folder_name}/templates/{self.name}"

        file_content = ""
        with open(file_path, 'rb') as file:
            file_content = file.read()

        # Set name as basename of file_path when name is not passed
        if name == "":
            name = os.path.basename(file_path)

        data = {}

        if name is not None:
            data["name"] = name

        if template_type is not None:
            data["type"] = template_type

        if output_type is not None:
            data["output_type"] = output_type

        if public is not None:
            data["public"] = public

        files = {
            "content": (file_path, file_content)
        }

        resp = self.conn.http_put_upload(url, data, files)
        outdata = response_object_or_error(Template, resp, 200)
        outdata.conn = self.conn

        return outdata

    @classmethod
    def list_templates(cls, conn, folder_name, page, page_size):
        """ List all templates """

        folder_name = folder_name.lstrip("/")
        if folder_name == "":
            url = f"{conn.url}/api/templates"
        else:
            url = f"{conn.url}/api/folders/{folder_name}/templates"

        resp = conn.http_get(url)
        templates = response_object_or_error(Template, resp, 200)

        def update_data(tmpl):
            tmpl.conn = conn

            return tmpl

        return list(map(update_data, templates))

    def get(self):
        """ Return a Template """

        folder_name = self.folder_name.lstrip("/")
        if folder_name == "":
            url = f"{self.conn.url}/api/templates/{self.name}"
        else:
            url = f"{self.conn.url}/api/folders/{self.folder_name}/templates/{self.name}"

        resp = self.conn.http_get(url)
        outdata = response_object_or_error(Template, resp, 200)
        outdata.conn = self.conn

        return outdata


    def update(self, name=None, content=None, template_type=None, output_type=None, public=None):
        """ Update Template """

        folder_name = self.folder_name.lstrip("/")
        if folder_name == "":
            url = f"{self.conn.url}/api/templates/{self.name}"
        else:
            url = f"{self.conn.url}/api/folders/{self.folder_name}/templates/{self.name}"

        resp = self.conn.http_put(
            url,
            {
                "name" : name,
                "content": content,
                "type": template_type,
                "output_type": output_type,
                "public": public
            }
        )

        # Update object name so deletion can be done from the same object after updation.
        if resp.status == 200 and name is not None:
            self.name = name

        outdata = response_object_or_error(Template, resp, 200)
        outdata.conn = self.conn

        return outdata


    def delete(self):
        """ Delete Template """

        folder_name = self.folder_name.lstrip("/")
        if self.folder_name == "":
            url = f"{self.conn.url}/api/templates/{self.name}"
        else:
            url = f"{self.conn.url}/api/folders/{folder_name}/templates/{self.name}"

        resp = self.conn.http_delete(url)
        return response_object_or_error(Template, resp, 204)
