# noqa # pylint: disable=missing-module-docstring
import json
import urllib3
from urllib3.filepost import encode_multipart_formdata

class APIError(Exception):
    """ APIError Exception """
    def __init__(self, resp):
        data = json_from_response(resp)
        self.message = data["error"]
        self.status_code = resp.status
        super().__init__(self.message)


class ConnectionBase:
    # noqa # pylint: disable=missing-class-docstring
    def __init__(self):
        self.token = ""
        self.user_id = ""

    def get_headers(self):
        """ Returns token and user-id as headers """

        headers = {'Content-Type': 'application/json'}

        if self.token != "":
            headers["Authorization"] = f"Bearer {self.token}"

        if self.user_id != "":
            headers["X-USER-ID"] = self.user_id

        return headers

    def http_post(self, url, data):
        """ Send HTTP Post Request with headers """

        http = urllib3.PoolManager()
        encoded_data = json.dumps(data).encode('utf-8')
        resp = http.request(
            'POST',
            url,
            body=encoded_data,
            headers=self.get_headers()
        )

        return resp


    def http_post_upload(self, url, meta, file_name="", file_content=""):
        """ Send HTTP Post Request by uploading a file """

        http = urllib3.PoolManager()

        fields = {
            "file": (file_name, file_content),
        }

        if meta is not None:
            fields["meta"] = json.dumps(meta)

        encoded_data, multipart_headers = encode_multipart_formdata(fields)

        # TODO: Explore `request` library to simplify sending multipart_formdata
        # multipart_headers is of the form,
        # 'multipart/form-data; boundary=a7b8ab6d919b6933490251e1d52f5551'
        # but we require headers['Content-Type'] to be 'Content-Type': 'multipart/form-data; boundary="a7b8ab6d919b6933490251e1d52f5551"'
        # hence extract int(boundary) from above string assign to updated headers to take final form as,
        # {'Content-Type': 'multipart/form-data; boundary="a7b8ab6d919b6933490251e1d52f5551"', 'Authorization': 'Bearer NNN', 'USER_ID': N}

        headers = self.get_headers()

        boundary = multipart_headers.split("=")[1]
        multipart_header = f'multipart/form-data; boundary="{boundary}"'
        headers['Content-Type'] = multipart_header

        # Send the request and get the response
        resp = http.request(
            method="POST",
            url=url,
            body=encoded_data,
            headers=headers
        )

        return resp


    def http_put(self, url, data):
        """ Send HTTP Put Request with headers """

        http = urllib3.PoolManager()
        encoded_data = json.dumps(data).encode('utf-8')
        resp = http.request(
            'PUT',
            url,
            body=encoded_data,
            headers=self.get_headers()
        )

        return resp


    def http_delete(self, url):
        """ Send HTTP Delete Request """

        http = urllib3.PoolManager()
        resp = http.request(
            'DELETE',
            url,
            headers=self.get_headers()
        )

        return resp


    def http_get(self, url):
        """ Send HTTP Get request with headers """

        http = urllib3.PoolManager()
        resp = http.request(
            'GET',
            url,
            headers=self.get_headers()
        )

        return resp


# noqa # pylint: disable=too-few-public-methods
class Generic:
    """
    Generic class to convert dict into class object
    """

    def __init__(self, data):
        self.class_highlights = []

        for key, val in data.items():
            if isinstance(val, dict):
                setattr(self, key, self.__class__(data=val))
            elif isinstance(val, list):
                setattr(self, key, to_object(self.__class__, val))
            else:
                self.class_highlights.append(val)
                setattr(self, key, val)


    def __str__(self):
        # Some response may have 'int' values, convert them into 'str'
        # Example: id, template_id .. etc
        highlights = [str(item) for item in self.class_highlights]
        return f'<{self.__class__.__name__}({", ".join(highlights[0:2])},...)>'


def to_object(cls, data):
    # noqa # pylint: disable=missing-function-docstring
    if isinstance(data, list):
        return [
            (cls(data=item) if isinstance(item, dict) else item)
            for item in data
        ]

    return cls(data=data)


def json_from_response(resp):
    """ Wrapper to convert HTTP response into JSON """
    return json.loads(resp.data.decode('utf-8'))


def response_object_or_error(cls, resp, status_code=200):
    """ Return resp in object or raise APIError Exception if request fails """

    if resp.status == status_code:
        if status_code == 204:
            return None

        return to_object(cls, json_from_response(resp))

    raise APIError(resp)
