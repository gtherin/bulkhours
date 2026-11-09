// The editor's answers to the agent: files are read from open buffers when a
// student has unsaved changes, and every write lands as an undoable edit.
import * as vscode from "vscode";
import { sliceLines } from "../core/choices.ts";

export async function readTextFile(path: string, line?: number | null, limit?: number | null): Promise<string> {
  const doc = await vscode.workspace.openTextDocument(vscode.Uri.file(path));
  return sliceLines(doc.getText(), line, limit);
}

export async function writeTextFile(path: string, content: string): Promise<void> {
  const uri = vscode.Uri.file(path);
  const open = vscode.workspace.textDocuments.find((d) => d.uri.fsPath === uri.fsPath);
  if (!open) {
    await vscode.workspace.fs.writeFile(uri, new TextEncoder().encode(content));
    return;
  }
  const edit = new vscode.WorkspaceEdit();
  edit.replace(uri, new vscode.Range(0, 0, open.lineCount, 0), content);
  if (!(await vscode.workspace.applyEdit(edit))) throw new Error(`the editor refused the edit of ${path}`);
  await open.save();
}
