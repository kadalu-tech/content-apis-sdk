import ContentAPIAuthError from './helpers';
import jsonFromResponse from './helpers';
import Region from './regions';
import Folder from './folders';
import Document from './objects';
import fetch from 'node-fetch';

export default class ContentAPI {
    constructor(url, username=null, email=null, password=null, user_id=null, token=null) {
        this.url = url.replace(/^\/|\/$/g, '');

        console.log(username, password, this.url)

        if (username != null && password != null) {
            try {
                let resp = this.httpPost('/api/api-keys/', {
                    username: username,
                    password: password
                });

                console.log("response", resp);

                let resp_json = resp;
                this.user_id = resp_json["user_id"];
                this.token = resp_json["token"];
            } catch (error) {
                if (error instanceof ContentAPIAuthError) {
                    console.error("Authentication Error:", error.message);
                } else {
                    console.error("ERROR: ", error);
                }
            }
        }

        if (email != null && password != null) {
            let resp = this.httpPost('/api/api-keys/', {
                email: email,
                password: password
            })

            let resp_json = resp
            this.user_id = resp_json["user_id"]
            this.token = resp_json["token"]
        }

        if (user_id != null && token != null) {
            this.user_id = user_id
            this.token = token
        }
    }

    async httpPost(urlPath, body) {
        try {
            const response = await fetch(
                `${this.url}${urlPath}`,
                {
                    method: "POST",
                    headers: {
                        ...this.authHeaders(),
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(body)
                }
            );

            if (response.status == 401 || response.status == 403) {
                throw new ContentAPIAuthError((await response.json()).error);
            }

            const data = await response.json();
            if (data.error) {
                throw new Error(data.error);
            }

            return data;
        } catch (error) {
            // Handle the promise rejection here
            console.error("An error occurred:", error);
            throw error; // Re-throw the error to maintain consistent error handling
        }
    }


    async httpGet(urlPath, existsCheck=false) {
        const response = await fetch(
            `${this.url}${urlPath}`,
            {
                headers: {
                    ...this.authHeaders(),
                    'Content-Type': 'application/json'
                }
            }
        );

        if (response.status == 401 || response.status == 403) {
            throw new ContentAPIAuthError((await response.json()).error);
        }

        if (existsCheck) {
            return response.status == 200 ? true : false;
        }

        const data = await response.json();
        if (data.error) {
            throw new Error(data.error);
        }

        return data;
    }

    async httpDelete(urlPath) {
        const response = await fetch(
            `${this.url}${urlPath}`,
            {
                method: "DELETE",
                headers: {
                    ...this.authHeaders(),
                    'Content-Type': 'application/json'
                }
            }
        );

        if (response.status == 401 || response.status == 403) {
            throw new ContentAPIAuthError((await response.json()).error);
        }

        if (response.status !== 204) {
            const data = await response.json();
            if (data.error) {
                throw new Error(data.error);
            }
        }

        return;
    }

    static fromToken(url, user_id, api_key_id, token) {
        const mgr = new ContentAPI(url);
        mgr.user_id = user_id;
        mgr.api_key_id = api_key_id;
        mgr.token = token;

        return mgr;
    }

    authHeaders() {
        if (this.token != "") {
            let headers = {
            }
            if (this.token != "" && this.token != undefined) {
                headers["Authorization"] = `Bearer ${this.token}`
            }
            if (this.user_id != "" && this.user_id != undefined) {
                headers["X-USER-ID"] = this.user_id;
            }

            console.log("authHeaders", headers);

            return headers
        }

        return {}
    }

    async generateApiKey(username, password) {
        return await this.httpPost(
            `/api/v1/users/${username}/api-keys`, {password: password}
        )
    }

    static async login(url, username, password) {
        const mgr = new ContentAPI(url);
        const data = await mgr.generateApiKey(username, password)
        mgr.user_id = data.user_id;
        mgr.api_key_id = data.id;
        mgr.token = data.token;

        return mgr;
    }

    async logout() {
        if (this.api_key_id == "") {
            return;
        }

        await this.httpDelete(`/api/v1/api-keys/${this.api_key_id}`)
        this.api_key_id = '';
        this.user_id = '';
        this.token = '';

        return;
    }

    async createRegion(name, address) {
        return await Region.create(this, name, address);
    }

    async createFolder(name, region, immutable, version, lock, template) {
        return await Folder.create(this, name, region, immutable, version, lock, template);
    }

    async listFolders() {
        return await Folder.list(this);
    }

    folder(name) {
        return new Folder(this, name);
    }

    createObject(path, data, object_type, immutable = false, version = false, lock = false, template = null) {
        return Document.create(this, "/", path, data, object_type, immutable, version, lock, template);
    }

    uploadObject(filePath, object_type, path = "", immutable = false, version = false, lock = false, template = null) {
        return Document.upload(this, "/", filePath, object_type, path, immutable, version, lock, template);
    }

    listObjects() {
        return Document.list(this, "/");
    }

    object(path) {
        return new Document(this, "/", path);
    }







    async listPools(state=false) {
        return await Pool.list(this, state);
    }

    pool(name) {
        return new Pool(this, name);
    }

    node(name) {
        return new Node(this, name);
    }

    async addNode(name, endpoint="") {
        return await Node.add(this, name, endpoint);
    }

    async listNodes(state=false) {
        return await Node.list(this, state);
    }

    async createPool(name, distribute_groups, opts) {
        return await Pool.create(this, name, distribute_groups, opts);
    }

    async createUser(username, password, fullName="") {
        return await User.create(this, username, password, fullName);
    }

    async hasUsers() {
        return await User.hasUsers(this)
    }

    user(username) {
        return new User(this, username)
    }
}