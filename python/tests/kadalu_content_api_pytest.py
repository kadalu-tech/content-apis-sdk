import os
import sys
import json

# Get the absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the absolute path of the parent directory (containing kadalu_content_apis)
parent_dir = os.path.dirname(current_dir)

# Append the parent directory to the Python path
sys.path.append(parent_dir)

import kadalu_content_apis

USERNAME = os.environ.get("USERNAME")
API_KEY = os.environ.get("API_KEY")
URL = "http://localhost:5001"


def test_username_token_login():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )
    # verify token and user_id set properly
    assert conn.api_key == API_KEY
    assert conn.username == USERNAME


def test_create_template():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    content = """Hello <b>{{ data["first_name"] }}</b>"""
    tmpl = conn.create_template("simple-html", content, template_type="text", output_type="html")

    assert len(conn.list_templates()) == 1
    assert tmpl.name == "simple-html"


def test_list_templates():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    content = """Hello <b>{{ data["last_name"] }}</b>"""
    tmpl = conn.create_template("simple-html-2", content, template_type="text", output_type="html")

    assert len(conn.list_templates()) == 2


def test_get_template():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    tmpl = conn.template("simple-html")
    get_data = tmpl.get()

    assert get_data.name == "simple-html"
    assert get_data.type == "text"
    assert get_data.output_type == "html"


def test_update_template():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    tmpl = conn.template("simple-html-2")
    updated_tmpl = tmpl.update(public=True)

    assert updated_tmpl.public == True


def test_delete_template():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    tmpl = conn.template("simple-html-2")
    tmpl.delete()

    assert len(conn.list_templates()) == 1


def test_list_folders():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    folders = conn.list_folders()
    # Default folder(/), hence 1
    assert len(folders) == 1


def test_create_folder_without_region():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    folder = conn.create_folder("mydocs", template="simple-html")
    assert folder.name == "/mydocs"
    assert folder.region == "-"
    assert folder.immutable == False


def test_create_region():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    region = conn.create_region("in-blr", URL)
    assert region.name == "in-blr"
    assert region.address == URL


def test_create_folder_with_region():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    folder = conn.create_folder(name="mydocs_in_blr", region="in-blr", immutable=False, template="simple-html")
    assert folder.name == "/mydocs_in_blr"
    assert folder.region == "in-blr"
    assert folder.immutable == False


def test_update_folder():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    folder = conn.create_folder(name="mydocs_in_blr_2", region="in-blr", immutable=False)
    assert folder.name == "/mydocs_in_blr_2"
    assert folder.region == "in-blr"
    assert folder.immutable == False

    mydocs_in_blr_2 = conn.folder("mydocs_in_blr_2")
    updated_mydocs_in_blr_2 = mydocs_in_blr_2.update(immutable=True)
    assert updated_mydocs_in_blr_2.name == "/mydocs_in_blr_2"
    assert updated_mydocs_in_blr_2.immutable == True


def test_get_folder():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    mydocs_in_blr_2 = conn.folder("mydocs_in_blr_2")
    get_data = mydocs_in_blr_2.get()

    assert get_data.name == "/mydocs_in_blr_2"
    assert get_data.region == "in-blr"


def test_delete_folder():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    # List of folders before deletion
    folders = conn.list_folders()
    assert len(folders) == 4

    # Delete a folder
    mydocs_in_blr_2 = conn.folder("mydocs_in_blr_2")
    mydocs_in_blr_2.delete()

    # List of folders after deletion
    folders = conn.list_folders()
    assert len(folders) == 3


def test_create_default_object():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    data = json.dumps({
        "first_name": "ABC",
        "last_name": "EFG"
    })

    obj = conn.create_object(path="user-abc.json", data=data, object_type="json", template="simple-html")

    # Default objects will have `root_dir` as `/object-name`
    assert obj.root_dir == "/user-abc.json"
    assert obj.path == "/user-abc.json"
    assert obj.type == "json"


def test_get_default_object():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    obj = conn.object(path="user-abc.json")
    get_data = obj.get()

    # Default objects will have `root_dir` as `/object-name`
    assert get_data.root_dir == "/user-abc.json"
    assert get_data.path == "/user-abc.json"
    assert get_data.type == "json"


def test_create_object_with_folder():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    data = json.dumps({
        "first_name": "ABC",
        "last_name": "EFG",
        "middle_name": "IJK"
    })

    folder = conn.folder("mydocs_in_blr")
    obj = folder.create_object(path="user-abc2.json", data=data, object_type="json", template="simple-html")

    # Non-Default objects will have `root_dir` as `-`
    assert obj.root_dir == "-"
    assert obj.path == "/user-abc2.json"
    assert obj.type == "json"


def test_get_object_with_folder():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    folder = conn.folder("mydocs_in_blr")
    obj = folder.object(path="user-abc2.json")
    get_data = obj.get()

    # Default objects will have `root_dir` as `/object-name`
    assert get_data.root_dir == "-"
    assert get_data.path == "/user-abc2.json"
    assert get_data.type == "json"


def test_list_objects():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    # Lists default object(s)
    objects = conn.list_objects()
    assert len(objects) == 1

    # Lists object(s) with folder
    folder = conn.folder("mydocs_in_blr")
    objects = folder.list_objects()
    assert len(objects) == 1


def test_delete_default_object():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    # List of default objects before deletion
    objects = conn.list_objects()
    assert len(objects) == 1

    # Lists default object(s)
    obj = conn.object(path="user-abc.json")
    obj.delete()

    # List of default objects after deletion
    objects = conn.list_objects()
    assert len(objects) == 0


def test_delete_object_with_folder():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    # List of default objects before deletion
    folder = conn.folder("mydocs_in_blr")
    objects = folder.list_objects()
    assert len(objects) == 1

    # Delete object with folder
    obj = folder.object(path="user-abc2.json")
    obj.delete()

    # List of default objects after deletion
    objects = folder.list_objects()
    assert len(objects) == 0


def test_get_rendered_with_default_object():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    data = json.dumps({
        "first_name": "ABC",
        "last_name": "EFG"
    })

    obj = conn.create_object(path="user-abc.json", data=data, object_type="json", template="simple-html")

    # Default objects will have `root_dir` as `/object-name`
    assert obj.root_dir == "/user-abc.json"
    assert obj.path == "/user-abc.json"
    assert obj.type == "json"

    obj = conn.object("user-abc.json")
    rendered_data = obj.get_rendered()

    assert rendered_data == "Hello <b>ABC</b>"


def test_get_rendered_with_folder():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    data = json.dumps({
        "first_name": "ABC",
        "last_name": "EFG",
        "middle_name": "IJK"
    })

    folder = conn.folder("mydocs_in_blr")
    obj = folder.create_object(path="user-abc2.json", data=data, object_type="json", template="simple-html")

    # Non-Default objects will have `root_dir` as `-`
    assert obj.root_dir == "-"
    assert obj.path == "/user-abc2.json"
    assert obj.type == "json"

    obj = folder.object("user-abc2.json")
    rendered_data = obj.get_rendered()

    assert rendered_data == "Hello <b>ABC</b>"


def test_upload_templates_and_objects():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    template_file_path = "extra/templates.html"
    tmpl = conn.upload_template(file_path=template_file_path, name="simple-html-upload", template_type="text", output_type="html")

    tmpl = conn.template("simple-html-upload")
    get_template_data = tmpl.get()

    assert get_template_data.name == "simple-html-upload"

    object_file_path = "extra/objects.json"
    folder = conn.folder("mydocs_in_blr")
    obj = folder.upload_object(file_path=object_file_path, object_type="json", template="simple-html-upload", path="user-abc-upload.json")

    obj = folder.object("user-abc-upload.json")
    rendered_data = obj.get_rendered()

    assert rendered_data == "Hello from <b>KADALU TECHNOLOGIES</b>"


def test_folder_share_create():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    folder = conn.folder("mydocs_in_blr")

    share = folder.create_share(public=True)
    assert share.public == True

    share = folder.create_share(use_long_url=True)
    assert share.long_url_id != ""


def test_object_share_create():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    folder = conn.folder("mydocs_in_blr")
    obj = folder.object(path="user-abc2.json")

    share = obj.create_share(public=True)
    assert share.public == True

    share = obj.create_share(use_long_url=True)
    assert share.long_url_id != ""


def test_delete_shares():
    conn = kadalu_content_apis.Connection(
        url=URL,
        username=USERNAME,
        api_key=API_KEY
    )

    folder = conn.folder("mydocs_in_blr")
    share = folder.create_share(public=True)
    share_id = share.id
    share_obj = folder.share(share_id)
    share_obj.delete()

    folder = conn.folder("mydocs_in_blr")
    obj = folder.object(path="user-abc2.json")
    share = obj.create_share(public=True)
    share_id = share.id
    share_obj = obj.share(share_id)
    share_obj.delete()
