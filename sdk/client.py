import httpx
from sdk.account import Account
import base64
import time
import aiohttp
import asyncio
import json

class RestClient:
    chain_id: int
    client: httpx.Client
    baseUrl: str
    jsonRpcVersion: str = "2.0"
    jsonRpcId: str = "2.0"

    def __init__(self, baseUrl: str) -> None:
        self.baseUrl = baseUrl
        self.client = httpx.Client()

    def close(self):
        self.client.close()

    def jsonRpc(self, method, params):
        data = {
            "jsonrpc": self.jsonRpcVersion,
            "id": self.jsonRpcId,
            "method": method,
            "params": params
        }
        response = self.client.post(
            f"{self.baseUrl}",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        if response.status_code == 404:
            raise SuiRpcError(response.status_code, response.text)

        return response.json()

    def RpcDiscover(self):
        params = []
        return self.jsonRpc("rpc.discover", params)

    def BatchTransaction(self):
        pass

    def DryRunTransaction(self, tx_bytes):
        return
        params = [tx_bytes]
        print(tx_bytes)
        return self.jsonRpc("sui_dryRunTransaction", params)

    #  1. ImmediateReturn: immediately returns a response to client without waiting for any execution results.
    #       Note the transaction may fail without being noticed by client in this mode.
    #       After getting the response, the client may poll the node to check the result of the transaction.
    #  2. WaitForTxCert: waits for TransactionCertificate and then return to client.
    #  3. WaitForEffectsCert: waits for TransactionEffectsCert and then return to client.
    #       This mode is a proxy for transaction finality.
    #  4. WaitForLocalExecution: waits for TransactionEffectsCert and make sure the node executed the transaction locally before returning the client.
    #       The local execution makes sure this node is aware of this transaction when client fires subsequent queries.
    #       However if the node fails to execute the transaction locally in a timely manner, a bool type in the response is set to false to indicated the case.
    def ExecuteTransaction(self, tx_bytes, sig_scheme, signature, pub_key, request_type):
        params = [tx_bytes, sig_scheme, signature, pub_key, request_type]
        return self.jsonRpc("sui_executeTransaction", params)

    def GetCommitteeInfo(self, epoch: int):
        params = [epoch]
        return self.jsonRpc("sui_getCommitteeInfo", params)

    def GetEvents(self, query, cursor, limit: int, descending_order: bool):
        params = [query, cursor, limit, descending_order]
        return self.jsonRpc("sui_getEvents", params)

    def GetMoveFunctionArgTypes(self, package: str, module: str, function: str):
        params = [package, module, function]
        return self.jsonRpc("sui_getMoveFunctionArgTypes", params)

    def GetNormalizedMoveFunction(self, package: str, module_name: str, function_name: str):
        params = [package, module_name, function_name]
        return self.jsonRpc("sui_getNormalizedMoveFunction", params)

    def GetNormalizedMoveModule(self, package: str, module_name: str):
        params = [package, module_name]
        return self.jsonRpc("sui_getNormalizedMoveModule", params)

    def GetNormalizedMoveModulesByPackage(self, package):
        params = [package]
        return self.jsonRpc("sui_getNormalizedMoveModulesByPackage", params)

    def GetNormalizedMoveStruct(self, package: str, module_name: str, struct_name: str):
        params = [package, module_name, struct_name]
        return self.jsonRpc("sui_getNormalizedMoveStruct", params)

    def GetObject(self, objectID):
        params = [objectID]
        return self.jsonRpc("sui_getObject", params)

    def GetObjectsOwnedByObject(self, objectID):
        params = [objectID]
        return self.jsonRpc("sui_getObjectsOwnedByObject", params)

    def GetObjectsOwnedByAddress(self, accountAddress):
        params = [accountAddress]
        return self.jsonRpc("sui_getObjectsOwnedByAddress", params)

    def GetRawObject(self, objectID):
        params = [objectID]
        return self.jsonRpc("sui_getRawObject", params)

    def GetTotalTransactionNumber(self):
        params = []
        return self.jsonRpc("sui_getTotalTransactionNumber", params)

    def GetTransaction(self, digest):
        params = [digest]
        return self.jsonRpc("sui_getTransaction", params)

    # query options
    # `All`, `MoveFunction`, `InputObject`, `MutatedObject`, `FromAddress`, `ToAddress`
    def GetTransactions(self, query, cursor=None, limit=100, descending_order=False):
        params = [
            query, cursor, limit, descending_order
        ]
        return self.jsonRpc("sui_getTransactions", params)

    def GetTransactionsInRange(self, start, end):
        params = [start, end]
        return self.jsonRpc("sui_getTransactionsInRange", params)

    def MergeCoins(self, signer: str, primary_coin: str, coin_to_merge: str, gas: str, gas_budget: int):
        params = [signer, primary_coin, coin_to_merge,  gas, gas_budget]
        return self.jsonRpc("sui_mergeCoins", params)

    def MoveCall(self, signer: str, package_object_id: str, module: str, function: str, type_arguments: list[str], arguments: list[str], gas, gas_budget):
        params = [signer, package_object_id, module,  function,
                  type_arguments, arguments, gas, gas_budget]
        return self.jsonRpc("sui_moveCall", params)

    def Pay(self, signer: str, input_coins: list[str], recipients: list[str], amounts: list[int], gas: str, gas_budget: int):
        if len(recipients) != len(amounts):
            print("len(recipients) != len(amounts)")
            return
        params = [signer, input_coins, recipients, amounts, gas, gas_budget]
        return self.jsonRpc("sui_pay", params)

    def PayAllSui(self, signer: str, input_coins: list[str], recipients: str, gas_budget: int):
        params = [signer, input_coins, recipients, gas_budget]
        return self.jsonRpc("sui_payAllSui", params)

    def PaySui(self, signer: str, input_coins: list[str], recipients: list[str], amounts: list[int], gas_budget: int):
        if len(recipients) != len(amounts):
            print("len(recipients) != len(amounts)")
            return
        params = [signer, input_coins, recipients, amounts, gas_budget]
        return self.jsonRpc("sui_paySui", params)

    def Publish(self, sender: str, compiled_modules: str, gas: str, gas_budget: int):
        params = [sender, compiled_modules, gas, gas_budget]
        return self.jsonRpc("sui_publish", params)

    def SplitCoin(self, signer: str, coin_object_id: str, split_amounts: list[int], gas: str, gas_budget: int):
        params = [signer, coin_object_id, split_amounts, gas, gas_budget]
        return self.jsonRpc("sui_splitCoin", params)

    def SplitCoinEqual(self, signer: str, coin_object_id: str, split_count: int, gas: str, gas_budget: int):
        params = [signer, coin_object_id, split_count, gas, gas_budget]
        return self.jsonRpc("sui_splitCoinEqual", params)

    def SubscribeEvent(self, filter):
        params = [filter]
        return self.jsonRpc("sui_subscribeEvent", params)

    def TransferObject(self, signer: str, object_id: str, gas: str, gas_budget: int, recipient: str):
        params = [signer, object_id, gas, gas_budget, recipient]
        return self.jsonRpc("sui_transferObject", params)

    def TransferSui(self, signer: str, sui_object_id: str, gas_budget: int, recipient: str, amount: int):
        params = [signer, sui_object_id, gas_budget, recipient, amount]
        return self.jsonRpc("sui_transferSui", params)

    def TryGetPastObject(self, object_id: str, version: int):
        params = [object_id, version]
        return self.jsonRpc("sui_tryGetPastObject", params)


class SuiClient(RestClient):
    #  1. ImmediateReturn: immediately returns a response to client without waiting for any execution results.
    #       Note the transaction may fail without being noticed by client in this mode.
    #       After getting the response, the client may poll the node to check the result of the transaction.
    #  2. WaitForTxCert: waits for TransactionCertificate and then return to client.
    #  3. WaitForEffectsCert: waits for TransactionEffectsCert and then return to client.
    #       This mode is a proxy for transaction finality.
    #  4. WaitForLocalExecution: waits for TransactionEffectsCert and make sure the node executed the transaction locally before returning the client.
    #       The local execution makes sure this node is aware of this transaction when client fires subsequent queries.
    #       However if the node fails to execute the transaction locally in a timely manner, a bool type in the response is set to false to indicated the case.
    def __init__(self, baseUrl: str) -> None:
        super().__init__(baseUrl)
        self.semaphore = asyncio.Semaphore(5)

    async def AsyncGetObject(self, objectId):
        params = {
            "jsonrpc": self.jsonRpcVersion,
            "id": self.jsonRpcId,
            "method": "sui_getObject",
            "params": [objectId]
        }
        async with self.semaphore:
            async with self.session.post(self.baseUrl, data=json.dumps(params), headers={"Content-Type": "application/json"}) as response:
                return await response.text()

    def SignAndSubmitTransaction(self, account: Account, txBytes: str, sig_scheme="ED25519", request_type="WaitForLocalExecution"):
        pubBytes = account.publicKey().key.encode()
        pubB64 = bytes.decode(base64.b64encode(pubBytes))
        # Get txBytes base64 format
        signedTxBytes = account.sign(base64.b64decode(txBytes))
        signedData = bytes.decode(base64.b64encode(signedTxBytes))
        # Send
        result = self.ExecuteTransaction(
            txBytes, sig_scheme, signedData, pubB64, request_type)
        return result

    def GetSpecificObjectsOwnedByAddressSync(self, accountAddress, filterObjectType):
        accountObjects = self.GetObjectsOwnedByAddress(accountAddress)
        suiObjectIdList = []
        for object in accountObjects['result']:
            objectId = object['objectId']
            objectDetail = self.GetObject(objectId)
            objectType = objectDetail['result']['details']['data']['type']
            if 'fields' in objectDetail['result']['details']['data']:
                objectFields = objectDetail['result']['details']['data']['fields']
            if objectType == filterObjectType:
                suiObjectInfo = {}
                if objectFields != None and 'balance' in objectFields:
                    suiObjectInfo['balance'] = objectFields['balance']
                suiObjectInfo['objectId'] = objectId
                suiObjectIdList.append(suiObjectInfo)
        return suiObjectIdList

    async def GetSpecificObjectsOwnedByAddressMain(self, accountAddress, filterObjectType):
        accountObjects = self.GetObjectsOwnedByAddress(accountAddress)
        suiObjectIdList = []
        getObjectTasks = []
        for object in accountObjects['result']:
            objectId = object['objectId']
            getObjectTasks.append(asyncio.ensure_future(
                self.AsyncGetObject(objectId)))
        objects = await asyncio.gather(*getObjectTasks)
        for objectDetail in objects:
            objectDetail = json.loads(objectDetail)
            objectType = objectDetail['result']['details']['data']['type']
            if 'fields' in objectDetail['result']['details']['data']:
                objectFields = objectDetail['result']['details']['data']['fields']
            if objectType == filterObjectType:
                suiObjectInfo = {}
                if objectFields != None and 'balance' in objectFields:
                    suiObjectInfo['balance'] = objectFields['balance']
                suiObjectInfo['objectId'] = objectId
                suiObjectIdList.append(suiObjectInfo)
        return suiObjectIdList

    def GetSpecificObjectsOwnedByAddress(self, accountAddress, filterObjectType):
        self.session = aiohttp.ClientSession()
        loop = asyncio.get_event_loop()
        getObjectsTask = loop.create_task(self.GetSpecificObjectsOwnedByAddressMain(accountAddress, filterObjectType))
        loop.run_until_complete(getObjectsTask)
        loop.run_until_complete(self.session.close())
        loop.close()
        return getObjectsTask.result()

    def GetSuiObjectsOwnedByAddress(self, accountAddress):
        return self.GetSpecificObjectsOwnedByAddress(accountAddress, "0x2::coin::Coin<0x2::sui::SUI>")

    def GetSuiAmountOwnedByAddress(self, accountAddress, suiObjectList=None):
        suiBalance = 0
        if suiObjectList == None:
            suiObjectList = self.GetSuiObjectsOwnedByAddress(accountAddress)
        for suiObject in suiObjectList:
            suiBalance += suiObject['balance']
        return suiBalance

    def GetSuiObjectsByPayAmount(self, accountAddress, payAmount, suiObjectList=None):
        if suiObjectList == None:
            suiObjectList = self.GetSuiObjectsOwnedByAddress(accountAddress)
        suiBalance = 0
        objectIds = []
        for suiObject in suiObjectList:
            suiBalance += suiObject['balance']
            objectIds.append(suiObject['objectId'])
            if suiBalance >= payAmount:
                return objectIds
        return None

    def GetTransactionStatus(self, tx):
        count = 0
        while True:
            txStatus = self.GetTransaction(tx)
            if "effects" in txStatus['result'] and 'status' in txStatus['result']['effects']:
                return txStatus
            count += 1
            if count >= 5:
                return None
            time.sleep(1)


class FaucetClient:
    baseUrl: str
    restClient: RestClient

    def __init__(self, baseUrl: str, restClient: RestClient):
        self.baseUrl = baseUrl
        self.restClient = restClient

    def close(self):
        self.restClient.close()

    def Faucet(self, address: str):
        data = {"FixedAmountRequest": {"recipient": address}}

        response = self.restClient.client.post(
            f"{self.baseUrl}",
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=10)
        if response.status_code == 429:
            raise SuiRpcError(response.status_code,
                              "IP limit,Too many requests Limit")
        if response.status_code >= 400:
            raise SuiRpcError(response.status_code, response.text)
        return response.text


class SuiRpcError(Exception):
    def __init__(self, status_code, error):
        self.status_code = status_code
        self.error = error

    def __str__(self):
        return str(self.status_code) + "\n" + self.error
