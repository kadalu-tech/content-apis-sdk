class APIError extends Error {
    constructor(response) {
        super(`API Error: ${response.status}`);
        this.name = 'APIError';
        this.response = response;
    }
}

export default class Document {
    constructor(conn, name, path) {
        this.conn = conn;
        this.name = name;
        this.path = path;
    }

    static async create(conn, folder_name, path, data, object_type, threads, template) {
        folder_name = folder_name.replace(/^\//, "");
        let url;
        if (folder_name === "") {
            url = `/api/objects`;
        } else {
            url = `/api/folders/${folder_name}/objects`;
        }
        return await conn.httpPost(
            url,
            {
                path: path,
                type: object_type,
                data: data,
                threads: threads,
                template: template
            })
    }

    static async list(conn, folder_name) {
        folder_name = folder_name.replace(/^\//, "");
        let url;
        if (folder_name === "") {
            url = `/api/objects`;
        } else {
            url = `/api/folders/${folder_name}/objects`;
        }

        return await conn.httpGet(url);
    }

    async get() {
        const folderName = this.folderName.replace(/^\//, "");
        let url;
        if (folderName === "") {
            url = `/api/objects/${this.path}`;
        } else {
            url = `/api/folders/${folderName}/objects/${this.path}`;
        }

        return await this.conn.httpGet(url);
    }

    async update(path = null, data = null, object_type = null, template = null) {
        const folderName = this.folderName.replace(/^\//, "");
        let url;
        if (folderName === "") {
            url = `/api/objects`;
        } else {
            url = `/api/folders/${folderName}/objects/${this.path}`;
        }

        const requestData = {
            path: path,
            data: data,
            type: object_type,
            template: template
        };

        const resp = await conn.httpPut(url, requestData);

        // Update object name so deletion can be done from the same object after updation.
        if (resp.status === 200 && path !== null) {
            this.path = path;
        }

        return resp;
    }

    async delete() {
        return await this.conn.httpDelete(
            `/api/folders/${this.name}`
        )
    }

    async getRendered(template = "") {
        // Remove leading "/" from folder_name
        const folderName = this.folderName.replace(/^\//, "");

        let url;

        if (folderName === "") {
            url = `${this.conn.url}/api/content/objects/${this.path}`;
        } else {
            url = `${this.conn.url}/api/content/folders/${folderName}/objects/${this.path}`;
        }

        const resp = await this.conn.httpGet(url);

        if (resp.status !== 200) {
            throw new APIError(resp);
        }

        // Assuming resp.data is a string in utf-8 encoding
        return resp.data;
    }

    async createShare(isPublic=false, use_long_url=false, password="", use_token=false, disable=false, revoke=false, expire=false, role="") {
        return Share.create(this.conn, this.folder_name, this.path, isPublic, use_long_url, password, use_token, disable, revoke, expire, role)
    }

    async listShares() {
        return Share.list(this.conn, this.folder_name, this.path)
    }

    share(share_id) {
        return new Share(this.conn, this.folder_name, this.path, share_id)
    }
}
