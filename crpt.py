from colorama import Fore, Back, Style, init
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import cryptography.hazmat.backends.openssl.rsa as ts
import cryptography.hazmat.primitives._serialization as ser
from cryptography.hazmat.primitives import serialization, hashes


def derivepublickey(privkey: ts._RSAPublicKey):
    key = privkey
    return (
        key.public_key()
        .public_bytes(ser.Encoding.PEM, ser.PublicFormat.PKCS1)
        .decode("utf-8")
    )


def generatekey(keysize=1024):
    key = rsa.generate_private_key(public_exponent=65537, key_size=keysize)
    pubkey = derivepublickey(key)
    return (key, pubkey)


def encrypt(message: str, publickey: str):
    keybytes = publickey.encode("utf-8")
    messagebytes = message.encode("utf-8")
    loadedPublic = serialization.load_pem_public_key(keybytes)
    cipher = loadedPublic.encrypt(
        messagebytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return cipher


def decrypt(message: str, privatekey: str):
    # loadedPrivate = serialization.load_pem_private_key(privatekey, password=)
    decryptedString = privatekey.decrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return decryptedString.decode("utf-8")
