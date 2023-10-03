# Folders

## Creating a new Folder

To create a new folder with region,

First create a region with `create_region()`

```
region = conn.create_region("in-blr", URL)
```

Here,
- `in-blr` is the region name.
- `URL` is the URL of the region to be associated.

Then create a Folder with `create_folder()`

```
folder = conn.create_folder(name="mydocs_in_blr", region="in-blr", immutable=False, template="simple-html", lock=False, version=False)
```

Here,
- `name` is the name of Folder.

Optional Arguments,
- `region` is the region for which the Folder is associated.
- `immutable` sets if Folder can be modified or not.
- `template` is the name of Template for which Folder is associated. All objects inside the Folder will have this Templates.
- `lock` <>
- `version` <>

## Update Folders

Folders can be updated with `update()` on Folder instance.

```
mydocs_in_blr_2 = conn.folder("mydocs_in_blr_2")
updated_mydocs_in_blr_2 = mydocs_in_blr_2.update(immutable=True)
```

Updation of Folder can take following arguments,

- `name` Change Name of folder if it does not already exist.
- `region` Change Region of Folder.
- `template` Change Template of Folder.
- `immutable` Boolean argument to change Immutablity.
- `lock` Boolean argument to change Lock characterstic.
- `version` Boolean argument to change Version characterstic.

## List Folders

List of created Folders can be fetched with `list_folders()`

```
folders = conn.list_folders()
```

# Deleting Folders

Folders can be deleted with `delete()` on Folder instance.

```
mydocs_in_blr_2 = conn.folder("mydocs_in_blr")
mydocs_in_blr_2.delete()
```

Here,
- `mydocs_in_blr` is the name of the Folder to be deleted.
