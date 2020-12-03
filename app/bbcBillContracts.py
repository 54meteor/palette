from contracts import Contracts

class BbcBillContracts(Contracts):
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


    def testInFlow(self,amount,contracAddress,bbcBranch,bbcAddress):
        self.printO("test InFlow start")
        try:
            tx_hash = self.function.inFlow(amount,contracAddress,
            bbcBranch,bbcAddress
            ).transact()
        except ValueError as e:
            self.printE("transfer result is  " + e.args[0]['message'])
            return
        receipt = self.w3.eth.getTransactionReceipt(tx_hash)
        events = self.testEvents(receipt,"inFlow")
        if(events.contractAddress == contracAddress):
            self.printS("events is Successed")
        else:
            self.printE("events is Error")
        self.printO("test InFlow end")
        return receipt['transactionHash']


    def testRetrace(self,txid,amount,walletAddress,contractAddr,fee):
        self.printO("test Retrace start")
        txid = self.w3.toInt(txid)
        try:
            tx_hash = self.function.retrace(txid,amount,walletAddress,contractAddr,fee).transact()
        except ValueError as e:
            self.printE("transfer result is  " + e.args[0]['message'])
            return
        receipt = self.w3.eth.getTransactionReceipt(tx_hash)
        events = self.testEvents(receipt, "retrace")
        if (events.contractAddress == contractAddr):
            self.printS("events is Successed")
        else:
            self.printE("events is Error")
        self.printO("test Retrace end")


    def testWithDraw(self,txid,bbcBranch,walletAddress,contractAddr,amount,fee,rate):
        self.printO("test WithDraw start")
        try:
            tx_hash = self.function.withDraw(txid,bbcBranch,walletAddress,contractAddr,
                                         amount,fee,rate).transact()
        except ValueError as e:
            self.printE("transfer result is  " + e.args[0]['message'])
            return
        receipt = self.w3.eth.getTransactionReceipt(tx_hash)
        events = self.testEvents(receipt, "withDraw")
        if (events.contractAddress == contractAddr):
            self.printS("events is Successed")
        else:
            self.printE("events is Error")
        self.printO("test WithDraw end")


    def testTransferAdmin(self,walletAddress):
        self.printO("test transferAdminship start")
        self.printN("admin is: " + self.function.admin().call())
        self.printN("owner is: " + self.function.owner().call())
        self.printO("defaultAccout is admin: " + str(self.function.isAdmin().call()))
        self.printO("change admin is: " + walletAddress)
        self.function.transferAdminship(walletAddress).transact()
        self.printN("admin is: " + self.function.admin().call())
        self.printN("owner is: " + self.function.owner().call())
        self.printO("defaultAccout is admin: " + str(self.function.isAdmin().call()))
        self.printO("test transferAdminship end")


    def testAdmin(self):
        return self.function.isAdmin().call()


    def testEvents(self,hash,flag):
        log = ""
        self.printRed("============Something w3 Exception======================");
        if(flag == "inFlow"):
            log = self.contract.events.inflowEvent().processReceipt(hash)
        if(flag == "withDraw"):
            log = self.contract.events.withdrawEvent().processReceipt(hash)
        if (flag == "retrace"):
            log = self.contract.events.retraceEvent().processReceipt(hash)
        if (flag == "admin"):
            log = self.contract.events.AdminTransferred().processReceipt(hash)
        self.printRed("========================================================");
        self.printS(str(log[0]['args']))
        return log[0]['args']

