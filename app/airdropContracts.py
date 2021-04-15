from contracts import Contracts

class Airdrop(Contracts):

    def getContractName(self):
        self.printO("Contract Name is " + self.function.name().call())

    def deploy_contract(self,ctsAddr):
        if(self.abi == "" or self.bin == ""):
            self.printN("Deploying Contract... " + self.contractFileName)
            contract_info = self.getContract()
            self.abi = contract_info['abi']
            self.bin = contract_info['bin']
        tx_hash = self.w3.eth.contract(
            abi=self.abi,
            bytecode=self.bin).constructor(ctsAddr).transact()
        self.contractAddr = self.w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        self.printN("Deployde Contract... Address:" + self.contractAddr)
        self.initContract()

    def testInit(self,cts):
        self.printN("transfer token to airdrop contract")
        amount = 40000000 * self.DECIMAL
        cts.function.transfer(self.contractAddr,amount).transact()
        balance = cts.function.balanceOf(self.contractAddr).call()
        self.printO(self.contractAddr + " iso Balance has : " + str(balance) + "SWF")


    def testBalanceOfToken(self):
        self.printN(" testBalanceOfToken ")
        balance = self.function.balanceOf().call()
        self.printO(" Balance has : " + str(balance))



    def testSafeTransfer(self,to,amount,cts):
        self.printN(" SafeTransfer " )
        self.function.safeTransfer(to,amount * self.DECIMAL).transact()
        balance = cts.function.balanceOf(to).call()
        self.printO(to + " token Balance has : " + str(balance) + "SWF")
        balance = cts.function.balanceOf(self.contractAddr).call()
        self.printO(to + " contract Balance has : " + str(balance) + "SWF")


    def testBatchTransfer(self,tos,amounts,cts):
        self.printN(" BatchTransfer ")
        self.function.batchTransfer(tos, amounts).transact()
        balance = cts.function.balanceOf(self.contractAddr).call()
        self.printO(self.contractAddr + " Balance has : " + str(balance) + "SWF")


