description: An OS-level file encryption daemon built in Python, using watchdog to monitor directory events in real-time and hybrid AES-256-EAX + RSA-2048 cryptography to automatically secure files.

---

# CipherHook — OS-Level File Encryption

[< Back Home](/)

[< Projects](/projects)

An OS-level file encryption daemon built in Python. It uses the `watchdog` library to monitor directory events in real-time and applies hybrid AES-256-EAX + RSA-2048 cryptography to automatically secure files the moment they are written.

## Overview

CipherHook is an event-driven background service (daemon) that watches a directory tree and encrypts new files transparently. The primary goal is to combine the speed of symmetric encryption (AES) with the key-exchange security of asymmetric encryption (RSA), eliminating the performance bottleneck of RSA-only encryption and the key distribution problem of AES-only systems.

The system runs as a `watchdog` observer that triggers on file close events, encrypts the file in-place using a randomly generated session key, and then destroys the original plaintext. Encrypted files receive a `.ederLockAlgorithm` suffix to prevent re-encryption loops.

## Architecture

```
User creates file in watched directory
           |
           v
+-----------------------------+
|  Watchdog Observer          |
|  (FileSystemEventHandler)   |
|  triggers on-closed event   |
+-----------------------------+
           |
           v
+-----------------------------+
|  Encryption Engine          |
|  1. Generate random          |
|     16-byte session key     |
|  2. Compress with zlib      |
|  3. AES-256-EAX encrypt     |
+-----------------------------+
           |
           v
+-----------------------------+
|  RSA Key Wrapper            |
|  Encrypt session key with   |
|  RSA-2048 public key        |
+-----------------------------+
           |
           v
+-----------------------------+
|  Payload Packaging          |
|  Concatenate:                |
|  - encrypted session key    |
|  - AES nonce (16 bytes)     |
|  - AES authenticity tag     |
|  - encrypted content        |
|  Encode as Base64           |
+-----------------------------+
           |
           v
+-----------------------------+
|  Secure Write               |
|  Write .ederLockAlgorithm   |
|  file, unlink() original    |
+-----------------------------+
```

## Hybrid Cryptography Design

The encryption workflow combines two algorithms to get the best of both:

1. **AES-256-EAX (symmetric):** A random 16-byte session key is generated for each file. The file content is compressed with `zlib` and encrypted with AES in EAX mode, which provides both confidentiality and authenticity (the tag verifies the data wasn't tampered with).

2. **RSA-2048 (asymmetric):** The session key itself is encrypted with the RSA public key. To decrypt a file you need the RSA private key -- without it, the AES session key cannot be recovered and the file stays locked.

The final payload is: `encrypted session key + nonce + tag + encrypted content`, all Base64-encoded for portability.

## Key Components

### Watchdog File Monitor

Uses Python's watchdog library with an Observer and a custom FileSystemEventHandler. The on-closed event is the trigger -- it fires when a file is closed after being written, ensuring the file is complete before encryption starts.

A custom suffix filter (`.ederLockAlgorithm`) prevents the daemon from trying to encrypt files that are already encrypted, avoiding infinite loops.

### Encryption Engine

The `encrypt()` function:
- Reads the plaintext file
- Compresses it with `zlib`
- Generates a fresh 16-byte AES session key via get_random_bytes
- Encrypts the compressed data with AES-256-EAX
- Encrypts the session key with RSA-2048 public key
- Packages everything into a Base64 payload

### Decryption Engine

The `decrypt()` function reverses the process:
- Reads the `.ederLockAlgorithm` file
- Decodes the Base64 payload
- Extracts the RSA-encrypted session key (size determined by RSA key length)
- Extracts the 16-byte nonce and 16-byte tag
- Decrypts the session key with the RSA private key
- Decrypts the content with AES-EAX using the recovered session key
- Decompresses with `zlib` to recover the original plaintext

### Secure deletion policy

After successful encryption, the original plaintext file is removed via `path.unlink()`. This removes the plaintext copy from disk after the daemon processes a file — it is an application-level cleanup, not a low-level wipe that overwrites disk blocks.

CipherHook is an educational exploration of hybrid file encryption rather than a production-grade secure deletion system.

### Audit Logging

All encryption and decryption events are logged to `system.log` with timestamps, severity levels, and descriptive messages. This provides a traceable audit trail for compliance and debugging.

## Technology Stack

**Language:** Python 3.x

**Cryptography:** PyCryptodome (RSA-2048, AES-256-EAX)

**File monitoring:** Watchdog (event-driven filesystem observer)

**Path handling:** Pathlib (cross-platform file path manipulation)

**Compression:** Zlib (pre-encryption compression to reduce storage)

**Logging:** Python logging module (audit trail)

## Installation and Usage

### Prerequisites

- Python 3.10 or higher
- Pip (Python package manager)

### Setup

Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running the Daemon

Launch the main script:

```
python main.py
```

The daemon generates RSA key pairs on first run (if they don't exist) and then starts monitoring the configured directory. Follow the on-screen prompts to configure the watched directory and encryption/decryption mode.

## Repository

[github.com/EderGtz/CipherHook-File-Encrypt](https://github.com/EderGtz/CipherHook-File-Encrypt)

## Date

February 24, 2026