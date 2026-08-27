"""
RSA Key Pair Generator - Tkinter GUI
Builds on the existing generate/save/load/details functions and wraps
them in a simple desktop UI.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


# ---------------------------------------------------------------------------
# Core RSA logic (same as your script, but save functions now respect the
# `path` argument instead of a hardcoded location)
# ---------------------------------------------------------------------------

def generate_keypair(key_size=2048):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    public_key = private_key.public_key()
    return private_key, public_key


def save_private_key(private_key, path, password=None):
    if password:
        encryption_algorithm = serialization.BestAvailableEncryption(password.encode())
    else:
        encryption_algorithm = serialization.NoEncryption()

    pem_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm
    )

    with open(path, 'wb') as f:
        f.write(pem_bytes)


def save_public_key(public_key, path):
    pem_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open(path, 'wb') as f:
        f.write(pem_bytes)


def load_private_key(path, password=None):
    with open(path, 'rb') as f:
        data = f.read()
    return serialization.load_pem_private_key(
        data,
        password=password.encode() if password else None
    )


def load_public_key(path):
    with open(path, 'rb') as f:
        data = f.read()
    return serialization.load_pem_public_key(data)


def get_key_details(private_key):
    numbers = private_key.private_numbers()
    return {
        "key_size": private_key.key_size,
        "n": numbers.public_numbers.n,
        "e": numbers.public_numbers.e,
        "d": numbers.d,
    }


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------

class RSAApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RSA Key Pair Generator")
        self.geometry("640x560")
        self.minsize(560, 480)
        self.configure(bg="#1e1e2e")

        self.private_key = None
        self.public_key = None

        self._build_style()
        self._build_widgets()

    # -- styling -----------------------------------------------------------
    def _build_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        bg = "#1e1e2e"
        fg = "#f5f5f5"
        accent = "#8b5cf6"

        style.configure("TFrame", background=bg)
        style.configure("TLabel", background=bg, foreground=fg, font=("Segoe UI", 10))
        style.configure("Header.TLabel", background=bg, foreground=accent,
                         font=("Segoe UI", 16, "bold"))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.configure("Accent.TButton", background=accent, foreground="white")
        style.map("Accent.TButton", background=[("active", "#7c3aed")])
        style.configure("TCombobox", padding=4)
        style.configure("TEntry", padding=4)

    # -- layout --------------------------------------------------------------
    def _build_widgets(self):
        pad = {"padx": 12, "pady": 6}

        header = ttk.Label(self, text="🔐 RSA Key Pair Generator", style="Header.TLabel")
        header.pack(anchor="w", **pad)

        form = ttk.Frame(self)
        form.pack(fill="x", **pad)

        # Key size
        ttk.Label(form, text="Key size:").grid(row=0, column=0, sticky="w", pady=4)
        self.key_size_var = tk.StringVar(value="2048")
        key_size_box = ttk.Combobox(
            form, textvariable=self.key_size_var,
            values=["1024", "2048", "4096"], state="readonly", width=10
        )
        key_size_box.grid(row=0, column=1, sticky="w", padx=(8, 0))

        # Password
        ttk.Label(form, text="Password (optional):").grid(row=1, column=0, sticky="w", pady=4)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(form, textvariable=self.password_var, show="*", width=30)
        password_entry.grid(row=1, column=1, sticky="w", padx=(8, 0))

        form.columnconfigure(1, weight=1)

        # Buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", **pad)

        self.generate_btn = ttk.Button(
            btn_frame, text="Generate Key Pair", style="Accent.TButton",
            command=self.on_generate
        )
        self.generate_btn.pack(side="left")

        self.save_priv_btn = ttk.Button(
            btn_frame, text="Save Private Key...", command=self.on_save_private, state="disabled"
        )
        self.save_priv_btn.pack(side="left", padx=8)

        self.save_pub_btn = ttk.Button(
            btn_frame, text="Save Public Key...", command=self.on_save_public, state="disabled"
        )
        self.save_pub_btn.pack(side="left")

        # Status
        self.status_var = tk.StringVar(value="No key generated yet.")
        status_label = ttk.Label(self, textvariable=self.status_var, foreground="#a1a1aa")
        status_label.pack(anchor="w", padx=12)

        # Progress bar (indeterminate, shown while generating)
        self.progress = ttk.Progressbar(self, mode="indeterminate")
        self.progress.pack(fill="x", padx=12, pady=(4, 0))
        self.progress.pack_forget()  # hidden until needed

        # Details output
        details_frame = ttk.Frame(self)
        details_frame.pack(fill="both", expand=True, padx=12, pady=(10, 12))

        ttk.Label(details_frame, text="Key Details:").pack(anchor="w")

        self.details_text = tk.Text(
            details_frame, wrap="word", height=14, bg="#282838", fg="#e5e5e5",
            insertbackground="#e5e5e5", relief="flat", padx=10, pady=10,
            font=("Consolas", 9)
        )
        self.details_text.pack(fill="both", expand=True, pady=(4, 0))
        self.details_text.configure(state="disabled")

        # Load section
        load_frame = ttk.Frame(self)
        load_frame.pack(fill="x", padx=12, pady=(0, 12))

        ttk.Button(load_frame, text="Load Public Key...", command=self.on_load_public).pack(side="left")
        ttk.Button(load_frame, text="Load Private Key...", command=self.on_load_private).pack(side="left", padx=8)

    # -- helpers -------------------------------------------------------------
    def _set_details_text(self, text):
        self.details_text.configure(state="normal")
        self.details_text.delete("1.0", "end")
        self.details_text.insert("1.0", text)
        self.details_text.configure(state="disabled")

    def _wrap(self, value, width=64):
        s = str(value)
        return "\n".join(s[i:i + width] for i in range(0, len(s), width))

    # -- actions -------------------------------------------------------------
    def on_generate(self):
        try:
            key_size = int(self.key_size_var.get())
        except ValueError:
            messagebox.showerror("Invalid key size", "Please choose a valid key size.")
            return

        password = self.password_var.get().strip() or None

        self.generate_btn.config(state="disabled")
        self.save_priv_btn.config(state="disabled")
        self.save_pub_btn.config(state="disabled")
        self.status_var.set(f"Generating {key_size}-bit RSA key pair...")
        self.progress.pack(fill="x", padx=12, pady=(4, 0))
        self.progress.start(10)

        def work():
            try:
                private_key, public_key = generate_keypair(key_size)
            except Exception as e:
                self.after(0, lambda: self._on_generate_error(e))
                return
            self.after(0, lambda: self._on_generate_done(private_key, public_key, password))

        threading.Thread(target=work, daemon=True).start()

    def _on_generate_error(self, error):
        self.progress.stop()
        self.progress.pack_forget()
        self.generate_btn.config(state="normal")
        self.status_var.set("Error while generating key.")
        messagebox.showerror("Generation failed", str(error))

    def _on_generate_done(self, private_key, public_key, password):
        self.private_key = private_key
        self.public_key = public_key
        self._last_password = password

        self.progress.stop()
        self.progress.pack_forget()
        self.generate_btn.config(state="normal")
        self.save_priv_btn.config(state="normal")
        self.save_pub_btn.config(state="normal")
        self.status_var.set("Key pair generated successfully.")

        details = get_key_details(private_key)
        text = (
            f"Key size : {details['key_size']} bits\n"
            f"Public exponent (e): {details['e']}\n\n"
            f"Modulus (n):\n{self._wrap(details['n'])}\n\n"
            f"Private exponent (d):\n{self._wrap(details['d'])}\n"
        )
        self._set_details_text(text)

    def on_save_private(self):
        if not self.private_key:
            return
        path = filedialog.asksaveasfilename(
            title="Save private key",
            defaultextension=".pem",
            initialfile="private_key.pem",
            filetypes=[("PEM files", "*.pem"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            save_private_key(self.private_key, path, password=getattr(self, "_last_password", None))
            self.status_var.set(f"Private key saved to {path}")
        except Exception as e:
            messagebox.showerror("Save failed", str(e))

    def on_save_public(self):
        if not self.public_key:
            return
        path = filedialog.asksaveasfilename(
            title="Save public key",
            defaultextension=".pem",
            initialfile="public_key.pem",
            filetypes=[("PEM files", "*.pem"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            save_public_key(self.public_key, path)
            self.status_var.set(f"Public key saved to {path}")
        except Exception as e:
            messagebox.showerror("Save failed", str(e))

    def on_load_public(self):
        path = filedialog.askopenfilename(
            title="Load public key",
            filetypes=[("PEM files", "*.pem"), ("All files", "*.*")]
        )
        if not path:
            return
        try:
            self.public_key = load_public_key(path)
            numbers = self.public_key.public_numbers()
            text = (
                f"Loaded public key from:\n{path}\n\n"
                f"Public exponent (e): {numbers.e}\n\n"
                f"Modulus (n):\n{self._wrap(numbers.n)}\n"
            )
            self._set_details_text(text)
            self.status_var.set("Public key loaded.")
        except Exception as e:
            messagebox.showerror("Load failed", str(e))

    def on_load_private(self):
        path = filedialog.askopenfilename(
            title="Load private key",
            filetypes=[("PEM files", "*.pem"), ("All files", "*.*")]
        )
        if not path:
            return

        password = self.password_var.get().strip() or None
        try:
            self.private_key = load_private_key(path, password=password)
            self.public_key = self.private_key.public_key()
            self.save_priv_btn.config(state="normal")
            self.save_pub_btn.config(state="normal")
            details = get_key_details(self.private_key)
            text = (
                f"Loaded private key from:\n{path}\n\n"
                f"Key size : {details['key_size']} bits\n"
                f"Public exponent (e): {details['e']}\n\n"
                f"Modulus (n):\n{self._wrap(details['n'])}\n\n"
                f"Private exponent (d):\n{self._wrap(details['d'])}\n"
            )
            self._set_details_text(text)
            self.status_var.set("Private key loaded.")
        except TypeError:
            messagebox.showerror(
                "Password required",
                "This key is encrypted. Enter its password in the field above and try again."
            )
        except Exception as e:
            messagebox.showerror("Load failed", str(e))


if __name__ == "__main__":
    app = RSAApp()
    app.mainloop()


    print("No woay")