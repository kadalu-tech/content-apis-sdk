export default class ContentAPIAuthError extends Error {
    constructor(message) {
        super(message);
        this.name = this.constructor.name;
    }
}

function jsonFromResponse(resp) {
    return JSON.parse(resp.data.toString('utf-8'));
}

// const kadaluContentApis = require('./output_node.js');
// let conn = new kadaluContentApis.ContentAPI("http://localhost:5001", "vatsa287", "vatsa@kadalu.tech", "1234")