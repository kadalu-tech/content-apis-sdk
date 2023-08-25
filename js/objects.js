export default class Document {
    constructor(conn, name, path) {
        this.conn = conn;
        this.name = name;
        this.path = path;
    }

    static async create(conn, folder_name, path, data, object_type, immutable, version, lock, template) {
        folder_name = folder_name.replace(/^\//, "");
        let url;
        if (folder_name === "") {
            url = `${conn.url}/api/objects`;
        } else {
            url = `${conn.url}/api/folders/${folder_name}/objects`;
        }
        return await conn.httpPost(
            url,
            {
                path: path,
                type: object_type,
                data: data,
                immutable: immutable,
                version: version,
                lock: lock,
                template: template
            })
    }

    static async list(conn, folder_name) {
        folder_name = folder_name.replace(/^\//, "");
        let url;
        if (folder_name === "") {
            url = `${conn.url}/api/objects`;
        } else {
            url = `${conn.url}/api/folders/${folder_name}/objects`;
        }

        return await conn.httpGet(url);
    }

    async get() {
        const folderName = this.folderName.replace(/^\//, "");
        let url;
        if (folderName === "") {
            url = `${this.conn.url}/api/objects/${this.path}`;
        } else {
            url = `${this.conn.url}/api/folders/${folderName}/objects/${this.path}`;
        }

        return await this.conn.httpGet(url);
    }

    async update(path = null, data = null, object_type = null, template = null) {
        const folderName = this.folderName.replace(/^\//, "");
        let url;
        if (folderName === "") {
            url = `${this.conn.url}/api/objects`;
        } else {
            url = `${this.conn.url}/api/folders/${folderName}/objects/${this.path}`;
        }

        const requestData = {
            path: path,
            data: data,
            type: object_type,
            template: template
        };

        const resp = await this.conn.httpPut(url, requestData);

        // Update object name so deletion can be done from the same object after updation.
        if (resp.status === 200 && path !== null) {
            this.path = path;
        }

        // Is await required here?
        return resp;
    }

    async delete() {
        return await this.conn.httpDelete(
            `${this.conn.url}/api/folders/${this.name}`
        )
    }
}