from kadalu_content_apis.helpers import response_object_or_error

class Share:
    def __init__(self, conn, folder_name, path, share_id):
        """ Intialise Document/Object """
        self.conn = conn
        self.folder_name = folder_name
        self.path = path
        self.share_id = share_id


    @classmethod
    def create(cls, conn, folder_name, path, public, use_long_url, password, use_token, role):
        """ Create Share Instance """

        if path == "":
            url = f"{conn.url}/api/shares/folders/{folder_name}"
        else:
            url = f"{conn.url}/api/shares/folders/{folder_name}/objects/{path}"

        if folder_name == "/" and path != "":
            url = f"{conn.url}/api/shares/objects/{path}"

        resp = conn.http_post(
            url,
            {
                "public": public,
                "use_long_url": use_long_url,
                "password": password,
                "use_token": use_token,
                "role": role
            }
        )
        return response_object_or_error("Share", resp, 201)


    @classmethod
    def list(cls, conn, folder_name, path):
        """ List share(s) of both default("/") and with folder-name """

        if path == "":
            url = f"{conn.url}/api/shares/folders/{folder_name}"
        else:
            url = f"{conn.url}/api/shares/folders/{folder_name}/objects/{path}"

        if folder_name == "/" and path != "":
            url = f"{conn.url}/api/shares/objects/{path}"

        resp = conn.http_get(url)
        return response_object_or_error("Share", resp, 200)


    def delete(self):
        """ Delete object of both default("/") and with folder-name """

        url = f"{self.conn.url}/api/shares/{self.share_id}"
        resp = self.conn.http_delete(url)
        return response_object_or_error("Share", resp, 204)

