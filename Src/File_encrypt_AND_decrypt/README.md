# File Encryption Tool

A command-line program that reads a file and performs encryption or decryption using the `cryptography` library's Fernet symmetric encryption.

## Information

- Any file type can be encrypted — the program reads and writes in binary mode, so it isn't limited to `.txt`
- Generating a new key overwrites the old one in `secret.key` — any files encrypted with the old key can no longer be decrypted
- Encrypted files are saved with a `.enc` extension, replacing the original extension (e.g. `file.txt` → `file.enc`, `photo.jpg` → `photo.enc`)
- Decrypted files are saved with a `.dec` extension (e.g. `file.enc` → `file.dec`)
- `.enc` and `.dec` files are excluded via `.gitignore` — every user generates their own from their own input files and key
- Run the program from the terminal, passing an action and (where needed) a filename as arguments

## Execution

### 1. Generate a key (do this first, only once)

You can regenerate the key at any time, but doing so overwrites `secret.key`. The same key must be used for both encryption and decryption of a given file.

```bash
python main.py G          # short form
python main.py genkey     # long form
```

### 2. Encrypt a file

Works with any file type.

```bash
python main.py E file.txt        # short form
python main.py encrypt file.txt  # long form
```

This creates `file.enc`.

### 3. Decrypt a file

```bash
python main.py D file.enc        # short form
python main.py decrypt file.enc  # long form
```

This creates `file.dec`, containing the same binary data as the original input file.

## Limitations

- Decryption requires the exact key used for encryption — if the key is regenerated, previously encrypted files can no longer be decrypted
- The decrypted output always carries a `.dec` extension regardless of the original file type — you'll need to rename it manually to restore the correct extension (e.g. back to `.jpg` or `.txt`) if you want to open it normally
- Modifying an encrypted file in any way will cause decryption to fail
- No error handling yet for missing files, missing keys, or missing command-line arguments — the program will crash with a raw Python traceback in these cases