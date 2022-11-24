from __future__ import annotations

import hashlib

from . import ed25519

from bip_utils import Bip39SeedGenerator, Bip39MnemonicGenerator, Bip39WordsNum
from bip_utils import Bip32Ed25519Slip

         
SUI_BIP32_PATH: str = "m/44'/784'/0'/0'/{}'"   
class Account:
    accountAddress: str
    privateKey: ed25519.PrivateKey

    def __init__(
        self, accountAddress: str, privateKey: ed25519.PrivateKey
    ):
        self.accountAddress = accountAddress
        self.privateKey = privateKey

    def __eq__(self, other: Account) -> bool:
        return (
            self.accountAddress == other.accountAddress
            and self.privateKey == other.privateKey
        )

    def generateMnemonic(word_nums: int =Bip39WordsNum.WORDS_NUM_12):
        generator = Bip39MnemonicGenerator()
        mnemonic = generator.FromWordsNumber(word_nums)
        return mnemonic

    def loadKeyByMnemonic(mnemonic,index = 0) -> Account:
        seed_bytes = Bip39SeedGenerator(mnemonic).Generate()
        bip32_ctx = Bip32Ed25519Slip.FromSeedAndPath(seed_bytes, SUI_BIP32_PATH.format(index))
    
        privateKey = bip32_ctx.PrivateKey().Raw().ToHex()
        return Account.loadKey(privateKey)

    def generate() -> Account:
        privateKey = ed25519.PrivateKey.random()
        accountAddress = Account.publick2Address(privateKey.publicKey())
        return Account(accountAddress, privateKey)

    def loadKey(key: str) -> Account:
        privateKey = ed25519.PrivateKey.fromHex(key)
        accountAddress = Account.publick2Address(privateKey.publicKey())
        return Account(accountAddress, privateKey)

    def address(self):
        return self.accountAddress

    def sign(self, data: bytes) -> bytes:
        return self.privateKey.sign(data)

    def publicKey(self) -> ed25519.PublicKey:
        return self.privateKey.publicKey()

    def publick2Address(key:ed25519.PublicKey):
        hasher = hashlib.sha3_256()
        hasher.update(b"\x00" + key.key.encode())
        return hasher.digest()[0:20].hex()