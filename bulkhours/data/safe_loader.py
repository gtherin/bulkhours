import io
import base64
import pandas as pd
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


def key_from_password(password: str, salt: bytes = b"static_salt") -> bytes:
    """
    Derive a Fernet-compatible key from a user-chosen string.
    Same password + same salt => same key.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend(),
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def secure_save(df: pd.DataFrame, path: str, password: str, **kwargs) -> None:
    """
    Save a DataFrame to an encrypted file.
    Use .csv.enc or .parquet.enc as extension.
    """
    key = key_from_password(password)
    cipher = Fernet(key)

    if path.endswith(".parquet.enc"):
        raw = df.to_parquet(index=False)
    elif path.endswith(".csv.enc"):
        raw = df.to_csv(index=False).encode()
    else:
        raise ValueError("Path must end with .csv.enc or .parquet.enc")

    with open(path, "wb") as f:
        f.write(cipher.encrypt(raw))


def secure_load(path: str, password: str, **kwargs) -> pd.DataFrame:
    """
    Load a DataFrame from an encrypted file.
    """
    key = key_from_password(password)
    cipher = Fernet(key)

    with open(path, "rb") as f:
        decrypted = cipher.decrypt(f.read())

    if path.endswith(".parquet.enc"):
        return pd.read_parquet(io.BytesIO(decrypted))
    elif path.endswith(".csv.enc"):
        return pd.read_csv(io.BytesIO(decrypted))
    else:
        raise ValueError("Unknown file type")
