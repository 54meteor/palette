from contracts import Contracts

class TokenContracts(Contracts):
    def getContractName(self):
        self.printO("Contract Name is " + self.function.name().call())


    def getOwnerBalance(self):
        balance = self.function.balanceOf(self.w3.eth.defaultAccount).call()
        self.printO("Contract Owner Balance has : " + str(balance))


    def testBalanceOf(self,address):
        balance = self.function.balanceOf(address).call()
        self.printO(address + " Balance has : " + str(balance))
        return balance

    def testTransfer(self):
        self.printO("transfer from " + self.w3.eth.defaultAccount + " to " + self.accountList[1] + "amount:10000")
        self.function.transfer(self.accountList[1],10000).transact();
        balance = self.testBalanceOf(self.accountList[1])
        if(balance == 10000):
            self.printS("transfer result is : True")
        else:
            self.printE("transfer result is : False")
        self.testBalanceOf(self.w3.eth.defaultAccount)


    def testTransferZero(self):
        self.deploy_contract()
        try:
            self.printO("transfer from " + self.w3.eth.defaultAccount + " to " + self.ZERO + "amount:10000")
            self.function.transfer(self.ZERO, 10000).transact();
        except ValueError as e:
            self.printE("transfer result is  " + e.args[0]['message'])

        self.testBalanceOf(self.w3.eth.defaultAccount)
