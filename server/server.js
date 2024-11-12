const { createConnection, TextDocuments, ProposedFeatures, DiagnosticSeverity } = require('vscode-languageserver/node');

const connection = createConnection(ProposedFeatures.all);
const documents = new TextDocuments();
documents.listen(connection);

connection.onInitialize(() => ({
    capabilities: {
        textDocumentSync: documents.syncKind,
        completionProvider: { resolveProvider: true }
    }
}));

connection.onCompletion(() => [
    { label: 'phase1', kind: 6, detail: 'Defines a phase in Ordo pipeline' },
    { label: 'data_loader.getUniverse', kind: 2, detail: 'Fetches the SP500 universe' }
]);

connection.onDidChangeContent((change) => {
    const diagnostics = [];
    const text = change.document.getText();

    if (text.includes("undefined")) {
        diagnostics.push({
            severity: DiagnosticSeverity.Error,
            range: {
                start: { line: 0, character: 0 },
                end: { line: 0, character: 9 }
            },
            message: "'undefined' is not a recognized term in Ordo.",
            source: 'ordo-language-server'
        });
    }

    connection.sendDiagnostics({ uri: change.document.uri, diagnostics });
});

connection.listen();
