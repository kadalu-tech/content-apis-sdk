import Document from "./objects";

export default class Folder {
    constructor(conn, name) {
        this.conn = conn;
        this.name = name;
    }

    static async create(conn, name, region, version, template) {
        return await conn.httpPost(`/api/folders`, {
            name: name,
            region: region,
            version: version,
            template: template
        })
    }

    static async list(conn) {
        return await conn.httpGet(`/api/folders`)
    }

    async get() {
        return await this.conn.httpGet(
            `/api/folders/${this.name}`
        )
    }

    async update(name="", region="", version=false, template="") {
        return await conn.httpPut(`/api/folders/${this.name}`, {
            name: name,
            region: region,
            version: version,
            template: template
        })
    }

    async delete() {
        return await this.conn.httpDelete(
            `/api/folders/${this.name}`
        )
    }

    async createObject(path, data, object_type, version=false, template="") {
        return await Document.create(this.conn, this.name, path, data, object_type, version, template);
    }

    async listObjects() {
        return await Document.list(this.conn, this.name);
    }

    object(path) {
        return new Document(this.conn, this.name, path);
    }

    async createShare(isPublic=false, use_long_url=false, password="", use_token=false, disable=false, revoke=false, expire=false, role="") {
        return Share.create(this.conn, this.name, "", isPublic, use_long_url, password, use_token, disable, revoke, expire, role)
    }

    async listShares() {
        return Share.list(this.conn, this.name, "")
    }

    share(share_id) {
        return new Share(this.conn, this.name, "", share_id)
    }
}
