export default class Template {
    constructor(conn, name, path) {
        this.conn = conn;
        this.name = name;
    }

    static async create(conn, name, content, template_type, output_type, isPublic) {
        return await conn.httpPost(
            `/api/templates`,
            {
                name: name,
                content: content,
                type: template_type,
                output_type: output_type,
                public: isPublic
            })
    }

    static async list(conn) {
        return await conn.httpGet(`/api/templates`);
    }

    async get() {
        return await this.conn.httpGet(`/api/templates/${this.name}`);
    }

    async update(name = null, content = null, template_type = null, output_type = null, isPublic = null) {
        const requestData = {
            name: name,
            content: content,
            type: template_type,
            output_type: output_type,
            public: isPublic
        };

        const resp = await conn.httpPut(`/api/templates/${this.name}`, requestData);

        // Update object name so deletion can be done from the same object after updation.
        if (resp.status === 200 && name !== null) {
            this.name = name;
        }

        return resp;
    }

    async delete() {
        return await this.conn.httpDelete(
            `/api/folders/${this.name}`
        )
    }
}
