from contracts import Contracts

class TestContracts(Contracts):
    def getContractName(self):
        self.printO("Contract Name is " + self.function.name().call())

    def approve(self, address, amount):
        self.printO("Contract approve:" + address + " amount=" + str(amount  / self.DECIMAL))
        self.function.approve(address, amount).transact()

    def getOwnerBalance(self):
        balance = self.function.balanceOf(self.w3.eth.defaultAccount).call()
        self.printO("Contract Owner Balance has : " + str(balance))
        return balance

    def testBalanceOf(self, address):
        balance = self.function.balanceOf(address).call()
        self.printO(address + " Balance has : " + str(balance  / self.DECIMAL))
        return balance

    def testTransfer(self):
        self.printO("transfer from " + self.w3.eth.defaultAccount + " to " + self.accountList[1] + "amount:10000")
        self.function.transfer(self.accountList[1], 10000).transact()
        balance = self.testBalanceOf(self.accountList[1])
        if (balance == 10000):
            self.printS("transfer result is : True")
        else:
            self.printE("transfer result is : False")
        self.testBalanceOf(self.w3.eth.defaultAccount)


    def testTransfer1(self):
        self.printO("transfer from " + self.w3.eth.defaultAccount + " to " + self.accountList[1] + "amount:10000")
        self.function.transferd(self.w3.eth.defaultAccount,self.accountList[1], 10000).transact()
        balance = self.testBalanceOf(self.accountList[1])
        if (balance == 10000):
            self.printS("transfer result is : True")
        else:
            self.printE("transfer result is : False")
        self.testBalanceOf(self.w3.eth.defaultAccount)

    def testTransfer2(self):
        self.printO("transfer from " + self.w3.eth.defaultAccount + " to " + self.accountList[1] + "amount:10000")
        self.function.transfer1(self.w3.eth.defaultAccount,self.accountList[1], 10000).transact()
        balance = self.testBalanceOf(self.accountList[1])
        if (balance == 10000):
            self.printS("transfer result is : True")
        else:
            self.printE("transfer result is : False")
        self.testBalanceOf(self.w3.eth.defaultAccount)


    def testTransferZero(self):
        self.deploy_contract()
        try:
            self.printO("transfer from " + self.w3.eth.defaultAccount + " to " + self.ZERO + "amount:10000")
            self.function.transfer(self.ZERO, 10000).transact()
        except ValueError as e:
            self.printE("transfer result is  " + e.args[0]['message'])

        self.testBalanceOf(self.w3.eth.defaultAccount)

    def deploy_contract_no_owner(self):
        if (self.abi == "" or self.bin == ""):
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
