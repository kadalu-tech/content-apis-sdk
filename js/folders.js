import Document from "./objects";

export default class Folder {
    constructor(conn, name) {
        this.conn = conn;
        this.name = name;
    }

    static async create(conn, name, region, immutable, version, lock, template) {
        return await conn.httpPost(`/api/folders`, {
            name: name,
            region: region,
            immutable: immutable,
            version: version,
            lock: lock,
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

    async update(name=null, region=null, immutable=null, version=null, lock=null, template=null) {
        return await this.conn.httpPut(`/api/folders/${this.name}`, {
            name: name,
            region: region,
            immutable: immutable,
            version: version,
            lock: lock,
            template: template
        })
    }

    async delete() {
        return await this.conn.httpDelete(
            `/api/folders/${this.name}`
        )
    }

    async createObject(path, data, object_type, immutable=false, version=false, lock=false, template=null) {
        return await Document.create(this.conn, this.name, path, data, object_type, immutable, version, lock, template);
    }

    async listObjects() {
        return await Document.list(this.conn, this.name);
    }

    object(path) {
        return new Document(this.conn, this.name, path);
    }

    async createShare(public=false, use_long_url=false, password="", use_token=false, role="") {
        return Share.create(this.conn, this.name, "", public, use_long_url, password, use_token, role)
    }

    async listShares() {
        return Share.list(this.conn, this.name, "")
    }

    share(share_id) {
        return new Share(this.conn, this.name, "", share_id)
    }
}
