from kadalu_content_apis.helpers import response_object_or_error

class Template:
    def __init__(self, conn, name):
        """ Intialise Template """
        self.conn = conn
        self.name = name


    # TODO: Handle Invalid Region Name, when only name is passed.
    @classmethod
    def create(cls, conn, name, content, template_type, output_type, public):
        """ Create template """

        resp = conn.http_post_upload(
            f"{conn.url}/api/templates",
            {
                "name" : name,
                "content": content,
                "type": template_type,
                "output_type": output_type,
                "public": public

            }
        )
        return response_object_or_error("Template", resp, 201)


    @classmethod
    def upload(cls, conn, file_path, template_type, name, output_type, public):

        file_content = ""
        with open(file_path, "r") as file:
            file_content = file.read()

        # Set name as basename of file_path when name is not passed
        if name == "":
            name = os.path.basename(file_path)

        meta = {
                "name" : name,
                "type": template_type,
                "output_type": output_type,
                "public": public
        }

        resp = conn.http_post_upload(
            f"{conn.url}/api/templates",
            meta, file_path, file_content
        )
        return response_object_or_error("Template", resp, 201)


    @classmethod
    def list_templates(cls, conn):
        """ List all templates """

        resp = conn.http_get(
            f"{conn.url}/api/templates"
        )
        return response_object_or_error("Template", resp, 200)


    def get(self):
        """ Return a Template """

        resp = self.conn.http_get(
            f"{self.conn.url}/api/templates/{self.name}"
        )
        return response_object_or_error("Template", resp, 200)


    def update(self, name=None, content=None, template_type=None, output_type=None, public=None):
        """ Update Template """

        resp = self.conn.http_put(
            f"{self.conn.url}/api/templates/{self.name}",
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

        return response_object_or_error("Template", resp, 200)


    def delete(self):
        """ Delete Template """
        resp = self.conn.http_delete(f"{self.conn.url}/api/templates/{self.name}")
        return response_object_or_error("Template", resp, 204)
