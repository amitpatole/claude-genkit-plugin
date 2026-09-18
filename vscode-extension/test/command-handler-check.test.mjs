import { test } from 'node:test';
import { strict as assert } from 'node:assert';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Read and parse package.json to get declared commands
const packageJsonPath = path.join(__dirname, '..', 'package.json');
const packageJsonContent = fs.readFileSync(packageJsonPath, 'utf8');
const packageJson = JSON.parse(packageJsonContent);

// Extract command IDs from package.json
const declaredCommands = packageJson.contributes.commands.map(cmd => cmd.command);
console.log(`Declared commands: ${declaredCommands.length}`);

// Read extension.ts to find registered commands
const extensionTsPath = path.join(__dirname, '..', 'src/extension.ts');
const extensionTsContent = fs.readFileSync(extensionTsPath, 'utf8');

// Find all registerCommand calls in extension.ts
const registerCommandRegex = /vscode\.commands\.registerCommand\s*\(\s*['"]([^'"]+)['"]/g;
const registeredCommands = [];
let match;

while ((match = registerCommandRegex.exec(extensionTsContent)) !== null) {
    registeredCommands.push(match[1]);
}

console.log(`Registered commands: ${registeredCommands.length}`);

// Test that all declared commands are registered
assert.ok(
    declaredCommands.every(cmd => registeredCommands.includes(cmd)),
    `The following commands are declared in package.json but have no handlers registered in extension.ts:\n` +
    declaredCommands
        .filter(cmd => !registeredCommands.includes(cmd))
        .map(cmd => `  - ${cmd}`)
        .join('\n')
);

// Test that all registered commands are declared
assert.ok(
    registeredCommands.every(cmd => declaredCommands.includes(cmd)),
    `The following commands are registered in extension.ts but not declared in package.json:\n` +
    registeredCommands
        .filter(cmd => !declaredCommands.includes(cmd))
        .map(cmd => `  - ${cmd}`)
        .join('\n')
);

// Test that both lists match exactly
test('Declared and registered commands must match exactly', () => {
    const declaredSet = new Set(declaredCommands);
    const registeredSet = new Set(registeredCommands);

    assert.strictEqual(
        declaredSet.size,
        registeredSet.size,
        `Command count mismatch: declared ${declaredSet.size} commands, registered ${registeredSet.size} commands`
    );

    for (const cmd of declaredSet) {
        assert.ok(
            registeredSet.has(cmd),
            `Declared command '${cmd}' is not registered`
        );
    }

    for (const cmd of registeredSet) {
        assert.ok(
            declaredSet.has(cmd),
            `Registered command '${cmd}' is not declared`
        );
    }
});
