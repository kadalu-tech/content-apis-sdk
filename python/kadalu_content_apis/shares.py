from kadalu_content_apis.helpers import response_object_or_error, Generic

class Share:
    def __init__(self, conn=None, folder_name=None, path=None, share_id=None, data=None):
        """ Intialise Document/Object """
        self.conn = conn
        self.folder_name = folder_name
        self.path = path
        self.id = share_id
        super().__init__(data)


    @classmethod
    def create(cls, conn, folder_name, path, public, use_long_url, password, use_token, disable, revoke, expire, role):
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
                "disable": disable,
                "revoke": revoke,
                "expire": expire,
                "role": role
            }
        )
        outdata = response_object_or_error(Share, resp, 201)
        outdata.conn = conn
        outdata.folder_name = folder_name
        outdata.path = path

        return outdata

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
        shares = response_object_or_error(Share, resp, 200)

        def update_data(share):
            share.conn = conn
            share.folder_name = folder_name
            share.path = path

            return share

        return list(map(update_data, shares))

    def update(self, disable=False, revoke=False, expire=False):
        """ Update share options """

        url = f"{self.conn.url}/api/shares/{self.id}"

        resp = self.conn.http_put(
            url,
            {
                "disable": disable,
                "revoke": revoke,
                "expire": expire
            }
        )
        outdata = response_object_or_error(Share, resp, 200)
        outdata.conn = self.conn

        return outdata

    def delete(self):
        """ Delete object of both default("/") and with folder-name """

        url = f"{self.conn.url}/api/shares/{self.id}"
        resp = self.conn.http_delete(url)
        return response_object_or_error(Share, resp, 204)

