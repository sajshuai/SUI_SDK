from sdk.client import SuiClient, FaucetClient
from sdk.common import *
from config import *
from sdk.account import Account
import sys

GAS_LIMIT = 10_000

client = SuiClient(NODE_URL)
faucetClient = FaucetClient(FAUCET_URL, client)
# TEST GetTotalTransactionNumber
print("GetTotalTransactionNumber",
      client.GetTotalTransactionNumber()['result'],"\n")
print("RPC Info:",client.RpcDiscover()['result']['info'],"\n")

# generate account
mnemonic = Account.generateMnemonic(12)
account = Account.loadKeyByMnemonic(mnemonic)
accountAddr = account.address()
print("Address:", accountAddr,"\n")

# # faucet
# faucetResult = faucetClient.Faucet(accountAddr)
# print(faucetClient,"\n")


# Get all my objects and sui balance
# TEST GetObjectsOwnedByAddress
# TEST GetObject
suiBalance = 0
suiObjects = client.GetSuiObjectsOwnedByAddress(accountAddr)
for object in suiObjects:
    suiBalance += object['balance']

if len(suiObjects) == 0:
    print("No SUI")
    sys.exit()

print(suiBalance / 10 ** SUI_DECIMALS, suiObjects, "\n")

# TEST GetCommitteeInfo
# result = client.GetCommitteeInfo(None)
# print(result, "\n")

# TEST GetEvents
# result = client.GetEvents(
#     {"Transaction": "lO4Bmtb1KPXlSw7bwEFZ+c2tlhQDcZ8Y6KRzaxBD5RA="}, None, 1, False)
# print(result, "\n")

# TEST GetMoveFunctionArgTypes
# result = client.GetMoveFunctionArgTypes("0x0000000000000000000000000000000000000002", "pay", "divide_and_keep")
# print(result, "\n")

# TEST GetNormalizedMoveFunction
# result = client.GetNormalizedMoveFunction("0x0000000000000000000000000000000000000002", "pay", "divide_and_keep")
# print(result, "\n")

# TEST GetNormalizedMoveModule
# result = client.GetNormalizedMoveModule("0x0000000000000000000000000000000000000002", "pay")
# print(result, "\n")

# TEST GetNormalizedMoveModulesByPackage
# result = client.GetNormalizedMoveModulesByPackage("0x0000000000000000000000000000000000000002")
# print(result, "\n")

# TEST GetNormalizedMoveStruct
# result = client.GetNormalizedMoveStruct("0x0000000000000000000000000000000000000002", "balance", "Supply")
# print(result, "\n")

# TEST GetTransaction
# tran =  client.GetTransaction("a61mCFK559oo1she1Qqr7m34Ifh+JfBSKUPrfAKr6XE=")
# print(tran,"\n")

# TEST GetTransactions
# trans = client.GetTransactions({"FromAddress": "0xc4173a804406a365e69dfb297d4eaaf002546ebd"},cursor="TLU65bBfCTqbTcE7Wc1CWJOWlw1Xl/VJBaXlW4Tz9vY=",limit=2)
# print(trans,"\n")

# TEST GetTransactionsInRange
# trans = client.GetTransactionsInRange(800000,800020)
# print(trans,"\n")

# TEST MergeCoins
# result = client.MergeCoins(
#     accountAddr, suiObjects[0]['objectId'], suiObjects[1]['objectId'], None, GAS_LIMIT)
# print(result)

# TEST MoveCall
# result = client.MoveCall(accountAddr, "0x0000000000000000000000000000000000000002", "pay", "join",
#                          ["0x2::sui::SUI"], [suiObjects[0]['objectId'], suiObjects[1]['objectId']],
#                          None, GAS_LIMIT)
# print(result)

# TEST Pay
# pay to myself
# result = client.Pay(accountAddr, [suiObjects[0]['objectId']], [accountAddr,accountAddr], [int(0.006 * 10**SUI_DECIMALS), int(0.006 * 10**SUI_DECIMALS)], None, GAS_LIMIT)
# print(result)

# TEST PayAllSui
# result = client.PayAllSui(accountAddr, [suiObjects[0]['objectId']], accountAddr, GAS_LIMIT)
# print(result)

# TEST PaySui
# result = client.PaySui(accountAddr, [suiObjects[0]['objectId']], [accountAddr, accountAddr], [
#                        int(0.006 * 10**SUI_DECIMALS), int(0.006 * 10**SUI_DECIMALS)], GAS_LIMIT)
# print(result)

# TEST Publish

# TEST SplitCoin
# result = client.SplitCoin(
#     accountAddr, suiObjects[0]['objectId'], [int(0.0001 * 10**SUI_DECIMALS),int(0.0001 * 10**SUI_DECIMALS)], None, GAS_LIMIT)
# print(result)

# TEST SplitCoinEqual
# result = client.SplitCoinEqual(
#     accountAddr, suiObjects[1]['objectId'], 3, None, GAS_LIMIT)
# print(result)

# TEST SubscribeEvent

# TEST TransferObject
# result = client.TransferObject(
#     accountAddr, suiObjects[1]['objectId'], None, GAS_LIMIT, accountAddr)
# print(result)

# TEST TransferSui
# result = client.TransferSui(
#     accountAddr, suiObjects[1]['objectId'], GAS_LIMIT, accountAddr, int(0.001 * 10**SUI_DECIMALS))
# print(result)

# TEST TryGetPastObject
# result = client.TryGetPastObject("0x0c793f8d25dbea7d879f942d283efdb8086a6b1a", 5)
# print(result)

# TEST ExecuteTransaction
# txBytes = result['result']['txBytes']
# result = client.SignAndSubmitTransaction(account, txBytes)
# print(result)
