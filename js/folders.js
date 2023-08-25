import Document from "./objects";

export default class Folder {
    constructor(conn, name) {
        this.conn = conn;
        this.name = name;
    }

    static async create(conn, name, region, immutable, version, lock, template) {
        return await conn.httpPost(`${conn.url}/api/folders`, {
            name: name,
            region: region,
            immutable: immutable,
            version: version,
            lock: lock,
            template: template
        })
    }

    static async list(conn) {
        return await conn.httpGet(`${conn.url}/api/folders`)
    }

    async get() {
        return await this.conn.httpGet(
            `${this.conn.url}/api/folders/${this.name}`
        )
    }

    async update(name=null, region=null, immutable=null, version=null, lock=null, template=null) {
        return await this.conn.httpPut(`${this.conn.url}/api/folders/${this.name}`, {
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
            `${this.conn.url}/api/folders/${this.name}`
        )
    }

    async createObject(path, data, object_type, immutable=False, version=False, lock=False, template=null) {
        return await Document.create(this.conn, this.name, path, data, object_type, immutable, version, lock, template);
    }

    async listObjects() {
        return await Document.list(this.conn, this.name);
    }

    object(path) {
        return new Document(this.conn, this.name, path);
    }

    // Shares SDKs
}