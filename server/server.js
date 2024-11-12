const { createConnection, TextDocuments, ProposedFeatures, CompletionItem, CompletionItemKind } = require('vscode-languageserver/node');

const connection = createConnection(ProposedFeatures.all);
const documents = new TextDocuments();
documents.listen(connection);

connection.onInitialize(() => ({
    capabilities: {
        textDocumentSync: documents.syncKind,
        completionProvider: { resolveProvider: true }
    }
}));

// Provide generic completions for objects, methods, and phases
connection.onCompletion(() => [
    { label: 'phase1', kind: CompletionItemKind.Keyword, documentation: 'Defines a new phase' },
    { label: 'phase2', kind: CompletionItemKind.Keyword, documentation: 'Defines a subsequent phase' },
    { label: 'object.method', kind: CompletionItemKind.Method, documentation: 'A generic method call on an object' },
    { label: 'variableName', kind: CompletionItemKind.Variable, documentation: 'A generic variable' }
]);

connection.listen();
