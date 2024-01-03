# noqa # pylint: disable=missing-module-docstring
import json

import requests


class APIError(Exception):
    """ APIError Exception """
    def __init__(self, resp):
        data = json_from_response(resp)
        self.message = data["error"]
        self.status_code = resp.status_code
        super().__init__(self.message)


class ExistsError(APIError):
    pass


class NotFoundError(APIError):
    pass


class ConnectionBase:
    # noqa # pylint: disable=missing-class-docstring
    def __init__(self):
        self.api_key = ""
        self.username = ""

    def get_headers(self, content_type = True):
        """ Returns Authorization and X-USERNAME headers """

        headers = {}
        if content_type:
            headers['Content-Type'] = 'application/json'

        if self.api_key != "":
            headers["Authorization"] = f"Bearer {self.api_key}"

        if self.username != "":
            headers["X-USERNAME"] = self.username

        return headers

    def http_post(self, url, data):
        """ Send HTTP Post Request with headers """

        resp = requests.post(
            url,
            json=data,
            headers=self.get_headers()
        )

        return resp


    def http_post_upload(self, url, data, files):
        """ Send HTTP Post Request by uploading a file """

        # Send the request and get the response
        resp = requests.post(
            url=url,
            data=data,
            files=files,
            headers=self.get_headers(content_type = False)
        )

        return resp

    def http_put_upload(self, url, data, files):
        """ Send HTTP Put Request by uploading a file """

        # Send the request and get the response
        resp = requests.put(
            url=url,
            data=data,
            files=files,
            headers=self.get_headers(content_type = False)
        )

        return resp

    def http_put(self, url, data):
        """ Send HTTP Put Request with headers """

        resp = requests.put(
            url,
            json=data,
            headers=self.get_headers()
        )

        return resp


    def http_delete(self, url):
        """ Send HTTP Delete Request """

        resp = requests.delete(
            url,
            headers=self.get_headers()
        )

        return resp


    def http_get(self, url):
        """ Send HTTP Get request with headers """

        resp = requests.get(
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
    return resp.json()


def response_object_or_error(cls, resp, status_code=200):
    """ Return resp in object or raise APIError Exception if request fails """

    if resp.status_code == status_code:
        if status_code == 204:
            return None

        return to_object(cls, json_from_response(resp))

    if resp.status_code == 409:
        raise ExistsError(resp)

    if resp.status_code == 404:
        raise NotFoundError(resp)

    raise APIError(resp)
