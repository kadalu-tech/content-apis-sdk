from content_apis.helpers import response_object_or_error

class Region:
    def __init__(self, conn, region, address):
        self.conn = conn
        self.region = region

    @classmethod
    def create(cls, conn, region, address):
        resp = conn.http_post(
            f"{conn.url}/api/regions/",
            {
                "region": region,
                "address": address
            }
        )

        return response_object_or_error("Region", resp, 201)