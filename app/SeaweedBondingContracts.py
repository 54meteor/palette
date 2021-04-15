from contracts import Contracts

class SeaweedBonding(Contracts):

    def getContractName(self):
        self.printO("Contract Name is " + self.function.name().call())

    def deploy_contract(self,ctsAddr,k,price):
        if(self.abi == "" or self.bin == ""):
            self.printN("Deploying Contract... " + self.contractFileName)
            contract_info = self.getContract()
            self.abi = contract_info['abi']
            self.bin = contract_info['bin']
        tx_hash = self.w3.eth.contract(
            abi=self.abi,
            bytecode=self.bin).constructor(ctsAddr,k,price).transact()
        self.contractAddr = self.w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        self.printN("Deployde Contract... Address:" + self.contractAddr)
        self.initContract()

    def testBuy(self,cts,amount,value):
        self.printN("buy token")
        self.function.buy(amount * self.DECIMAL,"code").transact({'value': value})
        balance = cts.function.balanceOf(self.contractAddr).call()
        self.printO(self.contractAddr + " token Balance has : " + str(balance / self.DECIMAL) + " SWF")
        eBalance = self.w3.eth.getBalance(self.contractAddr)
        self.printO(self.contractAddr + " contract HT Balance has : " + str(eBalance / self.DECIMAL) + " HT")

    def testCheckBuy(self,amount):
        self.printN("check buy amount")
        amount *= self.DECIMAL
        ethAmount = self.function.checkBuy(amount).call()
        self.printO("need ht:" + str(ethAmount / self.DECIMAL))
        return ethAmount

    def testGetAvailable(self):
        self.printN("check Available amount HT")
        amount =  self.function.getAvailable().call()
        self.printO("Available ht:" + str(amount / self.DECIMAL))
        return  amount


    def testCheckSell(self,amount):
        self.printN("check sell amount")
        amount *= self.DECIMAL
        ethAmount = self.function.checkSell(amount).call()
        self.printO("can receive HT:" + str(ethAmount / self.DECIMAL))
        return ethAmount

    def testSell(self,cts,amount):
        self.printN(" sell token " )
        self.function.sell(amount * self.DECIMAL).transact()
        balance = cts.function.balanceOf(self.contractAddr).call()
        self.printO(self.contractAddr + " token Balance has : " + str(balance / self.DECIMAL) + " SWF")
        eBalance = self.w3.eth.getBalance(self.contractAddr)
        self.printO(self.contractAddr + "  contract HT Balance has : " + str(eBalance / self.DECIMAL) + " HT")







