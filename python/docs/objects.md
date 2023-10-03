# Objects

## Creating Objects

Default Obects:
Objects are not present under any Folder but under Root.

To create a new `default` object,

Define data of object,
```
data = json.dumps({
    "first_name": "ABC",
    "last_name": "EFG"
})
```

And create a Object with `create_object()`

```
obj = conn.create_object(path="user-abc.json", data=data, object_type="json", template="simple-html"
```

Create Object under a Folder with `create_object` on Folder instance.

```
folder = conn.folder("mydocs_in_blr")
obj = folder.create_object(path="user-abc2.json", data=data, object_type="json", template="simple-html")
```

Here,
- `path` is the path of created Object.
- `data` is the data which Object holds.
- `object_type` is the type of data which Object holds.
- `template` is the name of Template which Object will be associated to. Rendering of the Object will be on the specified Template.
- `immutable` <>
- `version` <>
- `lock` <>

## Uploading Objects

Objects can be created by uploading the Object by specifing path.

Get the path of the object,
```
object_file_path = "extra/objects.json"
```

And upload with `upload_object` without directly on connection instance if it is a `default object` or use a Folder instance.

```
folder = conn.folder("mydocs_in_blr")
obj = folder.upload_object(file_path=object_file_path, object_type="json", template="simple-html-upload", path="user-abc-upload.json")
```

## Updating Objects

Created objects can be modified to change its path or characterstics.

Default objects can be modified with `update()` wheras,
Objects inside Folders can be mofified with `update()` on Folder instance.

```
folder = conn.folder("mydocs_in_blr")
object_file_path = "extra/objects.json"
obj = folder.update(data=data, object_type="json", template="simple-html", path="user-abc.json")
```

Here,
- `path` is the path of object to be updated.

List of optional arguments,
- `data` Data of object can be changed.
- `object_type` Type of Object can be changed based on change of data.
- `template` Template associated with Object can be changed.


## Listing Objects

Created Objects can be listed with `list()` on Folder instance for Object under Folders or only `list()` for `default objects`.

```
objects = conn.list_objects()

# Lists object(s) with Folder
folder = conn.folder("mydocs_in_blr")
objects = folder.list_objects()
```

## Deleting Objects

Objects can deleted with `delete()` on Folder instance for Objects under Folder or only `delete()` for `delfault objects`.

```
obj = conn.object(path="user-abc.json")
obj.delete()

# Delete object(s) with Folder
folder = conn.folder("my_docs_in_blr")
obj = folder.object(path="user-abc2.json")
obj.delete()
```
