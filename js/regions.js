export default class Region {
    constructor(conn, name) {
        this.conn = conn;
        this.name = name;
    }

    static async create(conn, name, address) {
        return await conn.httpPost('/api/regions', {
            name: name, address: address
        })
    }
}