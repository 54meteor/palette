from contracts import Contracts

class BbcExchangeContracts(Contracts):
    def deploy_contract(self):
        if(self.abi == "" or self.bin == ""):
            self.printN("Deploying Contract... " + self.contractFileName)
            contract_info = self.getContract()
            self.abi = contract_info['abi']
            self.bin = contract_info['bin']
        tx_hash = self.w3.eth.contract(
            abi=self.abi,
            bytecode=self.bin).constructor().transact()
        self.contractAddr = self.w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        self.printN("Deployde Contract... Address:" + self.contractAddr)
        self.initContract()


    def testCreateOrder(self,sellToken,sellAmount,buyToken,buyAmount,
                fee,goBetween,carryOut,blockHeight,
                ownerOtherWalletAddress,primaryKey):
        self.printO("test createOrder start")
        try:
            self.function.createOrder(
                sellToken,sellAmount,buyToken,buyAmount,
                fee,goBetween,carryOut,blockHeight,
                ownerOtherWalletAddress,primaryKey
            ).transact()
        except ValueError as e:
            self.printE("createOrder result is " + e.args[0])
            return
        self.printO("test createOrder end")


    def testGetOrderTradePairAmount(self,user,key):
        self.printO("test getOrderTradePairAmount start")
        try:
            amount = self.function.getOrderTradePairAmount(user,key).call()
        except ValueError as e:
            self.printE("getOrderTradePairAmount result is " + e.args[0])
            return 0
        self.printO("test getOrderTradePairAmount end")
        return amount


    def testGoBetween(self,orderAddress, sellToken, amount, buyToken,
            buyAmount, buyAddress, carryOutAddress, randIHash,
            randJHash, randKey, orderPrimaryKey, betweenPrimaryKey):
        self.printO("test GoBetween start")
        try:
            self.function.goBetween(
            orderAddress, sellToken, amount, buyToken,
            buyAmount, buyAddress, carryOutAddress, randIHash,
            randJHash, randKey, orderPrimaryKey, betweenPrimaryKey
            ).transact()
        except ValueError as e:
            self.printE("GoBetween result is " + e.args[0])
            return
        self.printO("test GoBetween end")

