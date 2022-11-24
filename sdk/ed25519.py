from __future__ import annotations
from nacl.signing import SigningKey, VerifyKey

class PrivateKey:
    LENGTH: int = 32

    key: SigningKey

    def __init__(self, key: SigningKey):
        self.key = key

    def __eq__(self, other: PrivateKey):
        return self.key == other.key

    def __str__(self):
        return self.hex()

    def fromHex(value: str) -> PrivateKey:
        if value[0:2] == "0x":
            value = value[2:]
        return PrivateKey(SigningKey(bytes.fromhex(value)))

    def hex(self) -> str:
        return f"0x{self.key.encode().hex()}"

    def publicKey(self) -> PublicKey:
        return PublicKey(self.key.verify_key)

    def random() -> PrivateKey:
        return PrivateKey(SigningKey.generate())

    def sign(self, data: bytes) -> bytes:
        return self.key.sign(data).signature


class PublicKey:
    LENGTH: int = 32

    key: VerifyKey

    def __init__(self, key: VerifyKey):
        self.key = key

    def __eq__(self, other: PrivateKey):
        return self.key == other.key

    def __str__(self) -> str:
        return f"0x{self.key.encode().hex()}"

    def verify(self, data: bytes, signature: bytes) -> bool:
        try:
            self.key.verify(data, signature)
        except:
            return False
        return True