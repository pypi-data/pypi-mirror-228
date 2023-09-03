import { ServerConnection } from '@jupyterlab/services';
import { PathExt } from '@jupyterlab/coreutils';
import { Signal } from '@lumino/signaling';
export const DRIVE_NAME = 'Box';
function arrayBufferToBase64(buffer) {
    let binary = '';
    const bytes = new Uint8Array(buffer);
    for (let i = 0; i < bytes.byteLength; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}
function base64DecodeAsBlob(text, type = 'text/plain;charset=UTF-8') {
    return fetch(`data:${type};base64,` + text).then(response => response.blob());
}
export class BoxDrive {
    constructor() {
        this._isDisposed = false;
        this._fileChanged = new Signal(this);
        this._boxIDMap = new Map([["", "0"], ["/", "0"]]);
        this._boxDirFileMap = new Map([["", true], ["/", true]]);
        this._accessToken = "";
    }
    get isDisposed() {
        return this._isDisposed;
    }
    dispose() {
        if (this.isDisposed) {
            return;
        }
        this._isDisposed = true;
        Signal.clearData(this);
    }
    set accessToken(accessToken) {
        this._accessToken = accessToken;
    }
    get name() {
        return DRIVE_NAME;
    }
    get serverSettings() {
        return ServerConnection.makeSettings();
    }
    get fileChanged() {
        return this._fileChanged;
    }
    async get(path, options) {
        if (!(options && 'content' in options && options.content) && this._boxDirFileMap.has(path)) {
            return {
                name: PathExt.basename(path),
                path: path,
                last_modified: '',
                created: '',
                format: null,
                mimetype: '',
                content: null,
                writable: true,
                type: this._boxDirFileMap.get(path) ? 'directory' : 'file'
            };
        }
        var client = new (new BoxSdk()).BasicBoxClient({
            accessToken: this._accessToken, noRequestMode: true
        });
        var id = await this.get_file_id(path);
        if (options && 'type' in options &&
            (options.type == 'file' || options.type == 'notebook')) {
            return this.get_file_content(client, id, path, options);
        }
        var opt = client.folders.get({ id: id, params: {
                fields: "name,item_collection"
            } });
        var r = await fetch(opt.url, {
            method: opt.method,
            headers: opt.headers,
            mode: opt.mode,
            cache: "no-store"
        });
        if (!r.ok) {
            if (r.status == 404) {
                return this.get_file_content(client, id, path, options);
            }
        }
        const res_json = await r.json();
        const content = [];
        for (const entry of res_json.item_collection.entries) {
            if (entry.type == "file") {
                const entry_ext = PathExt.extname(entry.name);
                var entry_type = 'file';
                if (entry_ext == ".ipynb") {
                    entry_type = 'notebook';
                }
                const subpath = this.build_path(path, entry.name, entry.id);
                content.push({
                    name: entry.name,
                    path: subpath,
                    created: '',
                    last_modified: '',
                    format: null,
                    mimetype: '',
                    content: null,
                    writable: true,
                    type: entry_type
                });
                this._boxDirFileMap.set(subpath, false);
            }
            else {
                const subpath = this.build_path(path, entry.name, entry.id);
                content.push({
                    name: entry.name,
                    path: subpath,
                    created: '',
                    last_modified: '',
                    format: null,
                    mimetype: '',
                    content: null,
                    writable: true,
                    type: 'directory'
                });
                this._boxDirFileMap.set(subpath, true);
            }
        }
        return {
            name: res_json.name,
            path: path,
            last_modified: '',
            created: '',
            format: null,
            mimetype: '',
            content,
            size: undefined,
            writable: true,
            type: 'directory'
        };
    }
    async getDownloadUrl(path) {
        var client = new (new BoxSdk()).BasicBoxClient({
            accessToken: this._accessToken, noRequestMode: true
        });
        const id = await this.get_file_id(path);
        var opt = client.files.getDownloadUrl({ id: id });
        var r = await fetch(opt.url, {
            method: opt.method,
            headers: opt.headers,
            mode: opt.mode,
            cache: "no-store"
        });
        const res_json = await r.json();
        if (!r.ok) {
            throw new Error();
        }
        return res_json.download_url;
    }
    async newUntitled(options) {
        var client = new (new BoxSdk()).BasicBoxClient({
            accessToken: this._accessToken, noRequestMode: true
        });
        let parentPath = '';
        if (options && options.path) {
            parentPath = options.path;
        }
        const type = (options === null || options === void 0 ? void 0 : options.type) || 'directory';
        var namebase = type === 'directory' ? 'Untitled Folder' : 'untitled';
        const ext = (options === null || options === void 0 ? void 0 : options.ext) || 'txt';
        const last_modified = new Date();
        var path;
        var entry;
        if (type === 'directory') {
            /*
            let i = 1;
            while (true) {
              name = `${name} ${i++}`;
            }
            */
            throw new Error('Method not implemented.');
        }
        else {
            for (let i = 0; true; i++) {
                var name;
                if (i == 0) {
                    name = `${namebase}`;
                }
                else {
                    name = `${namebase} ${i}`;
                }
                const newname = `${name}${ext}`;
                path = PathExt.join(parentPath, newname);
                let dirname = PathExt.dirname(path);
                var formData = new FormData();
                formData.append('parent_id', await this.get_file_id(dirname));
                const r = await this.upload_file_content(client, newname, "", formData, last_modified);
                if (!r.ok && r.status == 409) {
                    continue;
                }
                const res_json = await r.json();
                entry = res_json.entries[0];
                console.log(entry);
                break;
            }
        }
        let data = {
            name: entry.name,
            path: this.build_path(parentPath, entry.name, entry.id),
            created: new Date(entry.content_created_at).toISOString(),
            last_modified: new Date(entry.content_created_at).toISOString(),
            format: "text",
            mimetype: '',
            content: null,
            writable: true,
            type: 'file'
        };
        this._fileChanged.emit({
            type: 'new',
            oldValue: null,
            newValue: data
        });
        return data;
    }
    async delete(path) {
        var client = new (new BoxSdk()).BasicBoxClient({
            accessToken: this._accessToken, noRequestMode: true
        });
        const id = await this.get_file_id(path);
        const opt = await client.files.delete({ id });
        var r = await fetch(opt.url, {
            method: opt.method,
            headers: opt.headers,
            mode: opt.mode,
            cache: "no-store"
        });
        if (!r.ok) {
            throw new Error();
        }
        this._boxIDMap.delete(path);
        this._boxDirFileMap.delete(path);
    }
    async rename(path, newPath) {
        var client = new (new BoxSdk()).BasicBoxClient({
            accessToken: this._accessToken, noRequestMode: true
        });
        const id = await this.get_file_id(path);
        const newname = this.get_file_name(newPath);
        let dirname = PathExt.dirname(path);
        const opt = await client.files.updateInfo({ id, name: newname });
        var r = await fetch(opt.url, {
            method: opt.method,
            headers: opt.headers,
            mode: opt.mode,
            body: opt.body,
            cache: "no-store"
        });
        const res_json = await r.json();
        this.build_path(dirname, newname, id);
        return {
            name: newname,
            path: newPath,
            created: new Date(res_json.content_created_at).toISOString(),
            last_modified: new Date(res_json.content_modified_at).toISOString(),
            format: "text",
            mimetype: '',
            content: null,
            writable: true,
            type: 'file'
        };
    }
    async save(path, options) {
        var format = options === null || options === void 0 ? void 0 : options.format;
        const content = options === null || options === void 0 ? void 0 : options.content;
        var client = new (new BoxSdk()).BasicBoxClient({
            accessToken: this._accessToken, noRequestMode: true
        });
        let basename = PathExt.basename(path);
        let dirname = PathExt.dirname(path);
        var contentBlob;
        if (format == "base64") {
            contentBlob = await base64DecodeAsBlob(content);
        }
        else if (format == "json") {
            contentBlob = JSON.stringify(content, null, 2);
        }
        else if (format == "text") {
            contentBlob = content;
        }
        else {
            format = "text";
            contentBlob = content;
        }
        var formData = new FormData();
        var name;
        if (options && 'name' in options) {
            name = basename;
            formData.append('parent_id', await this.get_file_id(dirname));
        }
        else {
            name = this.get_file_name(path);
            formData.append('id', await this.get_file_id(path));
        }
        const last_modified = new Date();
        const r = await this.upload_file_content(client, name, contentBlob, formData, last_modified);
        console.log(r);
        const res_json = await r.json();
        console.log(res_json);
        this._fileChanged.emit({
            type: 'save',
            oldValue: null,
            newValue: contentBlob
        });
        let data;
        try {
            var id = await this.get_file_id(path);
            data = await this.get_file_content(client, id, path, options, last_modified);
        }
        catch (e) {
            data = {
                name,
                path,
                created: last_modified.toISOString(),
                last_modified: last_modified.toISOString(),
                format: format,
                mimetype: '',
                content: null,
                writable: true,
                type: 'file'
            };
        }
        return data;
    }
    async copy(path, toLocalDir) {
        var client = new (new BoxSdk()).BasicBoxClient({
            accessToken: this._accessToken, noRequestMode: true
        });
        let basename = PathExt.basename(path);
        let dirname = PathExt.dirname(path);
        const id = await this.get_file_id(path);
        const parent_id = await this.get_file_id(toLocalDir);
        const ext = PathExt.extname(basename);
        const namebase = basename.slice(0, basename.length - ext.length);
        for (let i = (dirname === toLocalDir ? 1 : 0); true; i++) {
            var name;
            if (i == 0) {
                name = `${namebase}`;
            }
            else {
                name = `${namebase} ${i}`;
            }
            const newname = `${name}${ext}`;
            const opt = await client.files.copy({
                id, name: newname, body: { parent: { id: parent_id } }
            });
            var r = await fetch(opt.url, {
                method: opt.method,
                headers: opt.headers,
                mode: opt.mode,
                body: opt.body,
                cache: "no-store"
            });
            if (!r.ok && r.status == 409) {
                continue;
            }
            const res_json = await r.json();
            const newpath = this.build_path(toLocalDir, newname, res_json.id);
            return {
                name: res_json.name,
                path: newpath,
                last_modified: new Date(res_json.content_modified_at).toISOString(),
                created: new Date(res_json.content_created_at).toISOString(),
                format: null,
                mimetype: '',
                content: '',
                writable: true,
                type: 'file'
            };
        }
    }
    async createCheckpoint(path) {
        return {
            id: 'test',
            last_modified: new Date().toISOString()
        };
    }
    async listCheckpoints(path) {
        return [
            {
                id: 'test',
                last_modified: new Date().toISOString()
            }
        ];
    }
    restoreCheckpoint(path, checkpointID) {
        return Promise.resolve(void 0);
    }
    deleteCheckpoint(path, checkpointID) {
        return Promise.resolve(void 0);
    }
    async get_file_content(client, id, path, options, last_modified) {
        var opt = client.files.get({ id: id, params: { fields: [
                    "id",
                    "name",
                    "content_created_at",
                    "content_modified_at",
                    "extension",
                    "item_status",
                    "lock",
                    "metadata",
                    "parent",
                    "path_collection",
                    "size"
                ].join(",") } });
        var r = await fetch(opt.url, {
            method: opt.method,
            headers: opt.headers,
            mode: opt.mode,
            cache: "no-store"
        });
        const res_json = await r.json();
        if (!r.ok) {
            throw new Error();
        }
        // console.log(res_json)
        const url = new URL(opt.url);
        var url_content = [url.protocol, '//', url.host, url.pathname + "/content"].join('');
        var r_content = await fetch(url_content, {
            method: opt.method,
            headers: opt.headers,
            mode: opt.mode,
            cache: "no-store"
        });
        let type;
        if (options && 'type' in options && options.type) {
            type = options.type;
        }
        else {
            type = "file";
        }
        /*
          File and Output Formats
          https://jupyterlab.readthedocs.io/en/stable/user/file_formats.html
        */
        let format;
        var mimetype = r_content.headers.get('content-type');
        if (mimetype == null) {
            mimetype = "text/plain";
            format = 'text';
        }
        else if (['ipynb'].includes(res_json.extension)) {
            mimetype = "";
            format = 'json';
        }
        else if ([
            'md',
            'yml', 'yaml',
            'json',
            'py',
        ].includes(res_json.extension) ||
            [
                "application/x-javascript",
                "image/svg+xml",
            ].includes(mimetype)) {
            mimetype = "text/plain";
            format = 'text';
        }
        else if (mimetype == "application/json") {
            format = 'json';
        }
        else if (mimetype && mimetype.split('/')) {
            if (['text'].includes(mimetype.split('/')[0])) {
                format = 'text';
            }
            else {
                format = 'base64';
            }
        }
        else {
            format = 'text';
        }
        var fileContent;
        if (format == "text") {
            fileContent = await r_content.text();
        }
        else if (type.toString() == "notebook") {
            fileContent = await r_content.json();
        }
        else {
            fileContent = arrayBufferToBase64(await r_content.arrayBuffer());
        }
        var last_modified_str;
        if (last_modified) {
            last_modified_str = last_modified.toISOString();
        }
        else {
            last_modified_str = new Date(res_json.content_modified_at).toISOString();
        }
        return {
            name: res_json.name,
            path: PathExt.join(path, res_json.name),
            created: new Date(res_json.content_created_at).toISOString(),
            last_modified: last_modified_str,
            format,
            mimetype,
            content: fileContent,
            writable: true,
            type
        };
    }
    async upload_file_content(client, name, contentBlob, formData, last_modified) {
        const file = new File([contentBlob], name, {
            type: "",
            lastModified: last_modified.getTime(),
        });
        formData.append(name, file);
        const optupload = await client.files.upload({ body: formData });
        if (optupload.headers && 'Content-Type' in optupload.headers) {
            delete optupload.headers['Content-Type'];
        }
        var r = await fetch(optupload.url, {
            method: optupload.method,
            headers: optupload.headers,
            body: optupload.body,
            mode: optupload.mode,
            cache: "no-store"
        });
        return r;
    }
    build_path(path, name, id) {
        const newpath = PathExt.join(path, name);
        this._boxIDMap.set(newpath, id);
        return newpath;
    }
    async get_file_id(path) {
        let id = this._boxIDMap.get(path);
        if (id) {
            return id;
        }
        let dirname = PathExt.dirname(path);
        if (dirname) {
            await this.get_file_id(dirname);
            await this.get(dirname, { content: true });
        }
        else {
            await this.get("", { content: true });
            return "0";
        }
        id = this._boxIDMap.get(path);
        if (id) {
            return id;
        }
        throw new Error('ID not found for path');
    }
    get_file_name(path) {
        let basename = PathExt.basename(path);
        return basename;
    }
}
