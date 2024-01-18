# noqa # pylint: disable=missing-module-docstring
from kadalu_content_apis.regions import Region
from kadalu_content_apis.folders import Folder
from kadalu_content_apis.objects import Document, DocumentThread
from kadalu_content_apis.templates import Template
from kadalu_content_apis.helpers import ConnectionBase, APIError, json_from_response, ExistsError, NotFoundError

DEFAULT_URL = "https://app.kadalu.tech"

class Connection(ConnectionBase):
    def __init__(self, username, api_key, url=DEFAULT_URL):
        """Intialise Connection and Login to Kadalu Content API"""
        self.url = url.strip("/")
        super().__init__()

        if username is not None and api_key is not None:
            self.username = username
            self.api_key = api_key


    @classmethod
    def from_env_file(cls, env_file_path):
        """
        Create the connection object from the given env file.

        Example env file:

        ```
        URL=https://app.kadalu.tech
        API_KEY=bc7889..
        USERNAME=aravindavk
        ```

        Usage:

        ```
        from kadalu_content_apis import Connection

        conn = Connection.from_env_file("/home/ubuntu/secrets/kca_prod.env")
        ```
        """
        env_vars = {}
        with open(env_file_path) as env_file:
            for line in env_file:
                if line.strip() == "":
                    continue
                key, value = line.split("=", 1)
                env_vars[key.strip()] = value.strip()

        return Connection(
            username=env_vars["USERNAME"],
            api_key=env_vars["API_KEY"],
            url=env_vars.get("URL", DEFAULT_URL)
        )

    def create_region(self, name, address):
        """ Create a new region """
        return Region.create(self, name, address)


    def create_folder(self, name, region="", threads=False):
        """ Create a new Folder """
        return Folder.create(self, name, region, threads)


    def list_folders(self, page=1, page_size=30):
        """ Return list of Folders """
        return Folder.list_folders(self, page, page_size)


    def folder(self, name):
        return Folder(self, name)

    @property
    def default_folder(self):
        return Folder(self, "/default")

    def thread(self, thread_id):
        return DocumentThread(self, thread_id)
