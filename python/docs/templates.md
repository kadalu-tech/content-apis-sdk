# Templates

## Creating a new Template

To create a new template,

Describe the content of template

```
content = """Hello <b>{{ data["first_name"] }}</b>"""
```

And create the template with `create_template()`

```
tmpl = conn.create_template("simple-html", content, template_type="text", output_type="html")
```

Here,

- `simple-html` is the name of the Template.
- `content` contains the content of the Template.
- `template_type` is set to `text` since content defined is in text format.
- `output_type` is set to `html` indicating, when object is rendered with this template, the output will be in html.


## Uploading a Template

Templates can be created by uploading the template by specifing path.

Get the file path of the template,

```
template_file_path = "extra/templates.html"
```

And upload using `upload_template()`,

```
tmpl = conn.upload_template(file_path=template_file_path, name="simple-html-upload", template_type="text", output_type="html")
```

Here,

- `file_path` is the path from where Template content is fetched.
- `name` is the name of Template created.


## Updating Templates

Created templates can be modified to change its name, content or characterstics.

Templates can be updated by calling `update()` on a template instance.

```
tmpl = conn.template("simple-html-2")
updated_tmpl = tmpl.update(public=True)
```

Templates can be modified for,

- `public` change visibility of Templates. Arguments are Boolean.
- `name` change name of Templates if that name does not already exist.
- `content` content of the Template can be updated, by specifying the `content` directy or by uplodading using `file_path`.
- `template_type` & `output_type` can also be updated.

## Listing Templates

List of created Templates can be fetched with `list_templates()`

```
conn.list_templates()
```

## Deleting Templates

Templates can be deleted with `delete()` on Template instance.

```
tmpl = conn.template("simple-html-2")
tmpl.delete()
```
