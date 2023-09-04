export default class ContentAPIAuthError extends Error {
    constructor(message) {
        super(message);
        this.name = this.constructor.name;
    }
}

function jsonFromResponse(resp) {
    return JSON.parse(resp.data.toString('utf-8'));
}
