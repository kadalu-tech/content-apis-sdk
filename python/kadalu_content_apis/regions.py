from kadalu_content_apis.helpers import response_object_or_error

class Region:
    def __init__(self, conn, name, address):
        """ Intialise Region """
        self.conn = conn
        self.name = name

    @classmethod
    def create(cls, conn, name, address):
        """ Create region """

        resp = conn.http_post(
            f"{conn.url}/api/regions/",
            {
                "name": name,
                "address": address
            }
        )
        return response_object_or_error("Region", resp, 201)
