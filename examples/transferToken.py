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
print("mnemonic:", mnemonic, "\n")
account = Account.loadKeyByMnemonic(mnemonic)
accountAddr = account.address()
print("Address:", accountAddr)

# # faucet
faucetResult = faucetClient.Faucet(accountAddr)
print(faucetResult)

suiObjects = client.GetSuiObjectsOwnedByAddress(accountAddr)
print(suiObjects, "\n")

if len(suiObjects) == 0:
    print("No SUI")
    sys.exit()

suiBalance = client.GetSuiAmountOwnedByAddress(accountAddr, suiObjects)
print(f"Address:{accountAddr}", f"Balance:{suiBalance/10**SUI_DECIMALS}", "\n")

toAddr = "0xe10a9c71cc35c2e83e5acbf0138a7d8aa0039d3b"
toAddrList = [toAddr, toAddr]

payAmount = int(0.00045 * 10**SUI_DECIMALS)
payAmountList = [payAmount, payAmount]
payAmountSum = sum(payAmountList)
payObjectIds = client.GetSuiObjectsByPayAmount(accountAddr,payAmountSum,suiObjects)

# pay
callResult = client.Pay(accountAddr, payObjectIds, toAddrList, payAmountList, None, GAS_LIMIT)
txBytes = callResult['result']['txBytes']
runCesult = client.SignAndSubmitTransaction(account, txBytes)
print(runCesult['result']['EffectsCert']['effects']['effects']['status'])

# # TEST PaySui
payObjectIds = client.GetSuiObjectsByPayAmount(accountAddr,payAmountSum)
callResult = client.PaySui(
    accountAddr, payObjectIds, toAddrList, payAmountList, GAS_LIMIT)
txBytes = callResult['result']['txBytes']
runCesult = client.SignAndSubmitTransaction(account, txBytes)
print(runCesult['result']['EffectsCert']['effects']['effects']['status'])

# TEST PayAllSui
callResult = client.PayAllSui(
    accountAddr, [suiObjects[0]['objectId']], accountAddr, GAS_LIMIT)
txBytes = callResult['result']['txBytes']
runCesult = client.SignAndSubmitTransaction(account, txBytes)
print(runCesult['result']['EffectsCert']['effects']['effects']['status'])
