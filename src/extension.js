const path = require('path');
const { workspace } = require('vscode');
const { LanguageClient, TransportKind } = require('vscode-languageclient/node');

function activate(context) {
    const serverModule = context.asAbsolutePath(path.join('server', 'server.js'));
    const serverOptions = {
        run: { module: serverModule, transport: TransportKind.ipc },
        debug: { module: serverModule, transport: TransportKind.ipc }
    };

    const clientOptions = {
        documentSelector: [{ scheme: 'file', language: 'ordo' }]
    };

    const client = new LanguageClient('ordoLanguageServer', 'Ordo Language Server', serverOptions, clientOptions);
    client.start();
}

exports.activate = activate;
