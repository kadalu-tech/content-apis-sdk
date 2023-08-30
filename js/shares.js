export default class Share {
    constructor(conn, folder_name, path, share_id) {
        this.conn = conn;
        this.folder_name = folder_name;
        this.path = path;
        this.share_id = share_id;
    }


    static async create(conn, folder_name, path, public, use_long_url, password, use_token, role) {
        folder_name = folder_name.replace(/^\//, "");
        let url;
        if (path === "") {
            url = `/api/shares/${folder_name}`;
        } else {
            url = `/api/shares/${folder_name}/objects/${path}`;
        }

        if (folder_name === "/" && path != "") {
            url = `/api/shares/objects/${path}`
        }

        return await conn.httpPost(
            url,
            {
                public: public,
                use_long_url: use_long_url,
                password: password,
                use_token: use_token,
                role: role
            })
    }


    static async list(conn, folder_name, path) {
        folder_name = folder_name.replace(/^\//, "");
        let url;
        if (path === "") {
            url = `/api/shares/folders/${folder_name}`;
        } else {
            url = `/api/shares/${folder_name}/objects/${path}`;
        }

        if (folder_name === "/" && path != "") {
            url = `/api/shares/objects/${path}`
        }

        return await conn.httpGet(url);
    }


    async delete() {
        return await this.conn.httpDelete(
            `/api/shares/${this.share_id}`
        )
    }
}
