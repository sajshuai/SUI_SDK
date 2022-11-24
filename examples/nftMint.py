from sdk.client import SuiClient, FaucetClient
from sdk.common import *
from config import *
from sdk.account import Account
import sys

GAS_LIMIT = 10_000

client = SuiClient(NODE_URL)
faucetClient = FaucetClient(FAUCET_URL, client)

# generate new account
mnemonic = Account.generateMnemonic(12)
print("mnemonic:", mnemonic)
account = Account.loadKeyByMnemonic(mnemonic)
accountAddr = account.address()
print("Address:", accountAddr)
# # faucet
faucetResult = faucetClient.Faucet(accountAddr)
print(faucetResult,"\n")

if len(client.GetSuiObjectsOwnedByAddress(accountAddr)) == 0:
    print("No SUI")
    sys.exit()

nftName = "nftMint"
nftDescription = "nftMint"
nftImageUrl = "nftMint"

# mint-nft  get transaction base64 data
objectId = "0x0000000000000000000000000000000000000002"
moduleName = "devnet_nft"
functionName = "mint"
typeArr = []
paramsArr = [nftName, nftDescription, nftImageUrl]
gasPayObjectId = None
callResult = client.MoveCall(accountAddr, objectId, moduleName,
                             functionName, typeArr, paramsArr, gasPayObjectId, GAS_LIMIT)

# mint-nft  submit transactions
if 'txBytes' in callResult['result']:
    txBytes = callResult['result']['txBytes']
    runCesult = client.SignAndSubmitTransaction(
        account, txBytes, request_type="ImmediateReturn")
    print("Submit", runCesult, "\n")

    tx = runCesult['result']['ImmediateReturn']['tx_digest']
    print("tx:", tx)

    txStatus = client.GetTransactionStatus(tx)
    print("txStatus", txStatus['result']['effects']['status'], "\n")

#NFT Transfer
nftObjects = client.GetSpecificObjectsOwnedByAddress(accountAddr,"0x2::devnet_nft::DevNetNFT")
if len(nftObjects) > 0:
    toAddr = "0xe10a9c71cc35c2e83e5acbf0138a7d8aa0039d3b"
    transferResult = client.TransferObject(
        accountAddr, nftObjects[0]['objectId'], None, GAS_LIMIT, toAddr)
        
    txBytes = transferResult['result']['txBytes']
    runCesult = client.SignAndSubmitTransaction(
        account, txBytes)
    print("tx:",runCesult['result']['EffectsCert']['certificate']['transactionDigest'])
    print("txStatus:", runCesult['result']['EffectsCert']['effects']['effects']['status'])