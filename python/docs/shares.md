# Shares

## Creating a Share

A share can be created with multiple variation both on characterstics of share and what it shares(Folder or Object).

Share types on characterstics:
- `public` When set creates a type of share which is accesible by Public
- `use_long_url` When set creates a share which accessible through a unique hash as URL.
- `password` Creates a shares with password and accessible through that password.
- `token` Creates a share with token and accessible through that token.

Creating a default Object share:

A defualt Object can be shared with `create_share()`

```
obj = conn.object(path="user-abc.json")

share = obj.create_share(public=True)
```

Creating a share of entire Folder:

Entire Folder can be shared, instead of sharing all Objects in a Folder with a common characterstic by calling `create_share()` on Folder instance.

```
folder = conn.folder("mydocs_in_blr")

share = folder.create_share(public=True)
```

Creating a share of a particular Object:

Individual Object under a Folder can be shared with `create_share()` on Object instance.

```
folder = conn.folder("mydocs_in_blr")
obj = folder.object(path="user-abc2.json")

share = obj.create_share(public=True)
```

All in above examples during `create_share()`, `public` is set to `True`.
Similarly can set any of chararcterstics as desribed above.

## Listing Shares

Shares created can be listed through `list()`.

Similar to `create_share()` mulitple ways to list based on Share,

Listing shares of defualt objects:

```
obj = conn.object(path="user-abc.json")

shares = obj.list_shares()
```

Listing shares of entire Folder:

```
folder = conn.folder("mydocs_in_blr")

shares = folder.list_shares()
```

Listing shares of a particular Object:

```
folder = conn.folder("mydocs_in_blr")
obj = folder.object(path="user-abc2.json")

shares = obj.list_shares()
```

## Deleting Shares

Shares can be deleted with `delete()` on Share object using `share_id` which can be fetched through `get()` or stored during creation of share.

```
folder = conn.folder("mydocs_in_blr")
share = folder.create_share(public=True)
share_id = share.id
share_obj = folder.share(share_id)
share_obj.delete()
```
