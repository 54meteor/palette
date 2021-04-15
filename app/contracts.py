import os
from web3 import Web3
import solcx


class Contracts():

    ETH_RPC = "http://127.0.0.1:8545"
    prefix = "<stdin>:"
    ROOT_PATH = os.path.split(os.path.abspath(__name__))[0]
    ZERO = "0x0000000000000000000000000000000000000000"
    DECIMAL = 10 ** 18
    NOTICE = "[\033[32mNOTICE\033[0m]"
    ERROR = "[\033[31mERROR\033[0m]"
    WARNING = "[\033[33mWARNING\033[0m]"
    OPERATING = "[\033[36mOPERATING\033[0m]"
    SUCCESS = "[\033[35mSUCCESS\033[0m]"
    abi = ""
    bin = ""

    def __init__(self,
                 contractName,
                 contractFileName,
                 version="0.5.16",
                 contractPath="/contracts/"):
        self.printN("Project Strat")
        self.contractName = contractName
        self.contractFileName = contractFileName
        self.w3 = Web3(Web3.HTTPProvider(self.ETH_RPC))
        self.version = version
        self.CONTRACTS_PATH = self.ROOT_PATH + contractPath
        solcx.install_solc(self.version)
        self.initAccounts()


    def initAccounts(self):
        self.accountList = self.w3.eth.accounts;
        self.w3.eth.defaultAccount = self.accountList[0]


    def setDefaultAccount(self,account):
        self.w3.eth.defaultAccount = account


    def getDefaultAccount(self):
        return self.w3.eth.defaultAccount


    def readContract(self):
        with open(self.CONTRACTS_PATH + self.contractFileName,'r') as fp:
            content = fp.read()
            return  content


    def compile_source_file(self):
        self.printN("Compiling Contract... " + self.contractFileName)
        return solcx.compile_source(
            self.readContract(),
            output_values=["abi", "bin"],
            solc_version=self.version,
            optimize = True
        )


    def getContract(self):
        return self.compile_source_file().get(self.prefix + self.contractName)


    def deploy_contract1(self,m,n):
        if(self.abi == "" or self.bin == ""):
            self.printN("Deploying Contract... " + self.contractFileName)
            # contract_info = self.compile_source_file1(self.CONTRACTS_PATH + self.contractFileName).get(self.prefix + self.contractName)
            # contract_info = self.compile_source_file1(self.CONTRACTS_PATH + self.contractFileName)
            # print(contract_info)
            contract_info = self.getContract()
            self.abi = contract_info['abi']
            self.bin = contract_info['bin']
        tx_hash = self.w3.eth.contract(
            abi=self.abi,
            bytecode=self.bin).constructor(m,n).transact()
        self.contractAddr = self.w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        self.printN("Deployde Contract... Address:" + self.contractAddr)
        self.initContract()


    def compile_source_file1(self,f):
        self.printN("Compiling Contract... " + self.contractFileName)
        return solcx.compile_files(
            f,
            output_values=["abi", "bin"],
            solc_version=self.version,
            optimize = True
        )

    def deploy_contract(self):
        if(self.abi == "" or self.bin == ""):
            self.printN("Deploying Contract... " + self.contractFileName)
            contract_info = self.getContract()
            self.abi = contract_info['abi']
            self.bin = contract_info['bin']
        tx_hash = self.w3.eth.contract(
            abi=self.abi,
            bytecode=self.bin).constructor(self.accountList[0]).transact()
        self.contractAddr = self.w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
        self.printN("Deployde Contract... Address:" + self.contractAddr)
        self.initContract()

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


    def initContract(self):
        self.printN("Testing Contract Ready ")
        checksum_address = self.w3.toChecksumAddress(self.contractAddr)
        self.contract = self.w3.eth.contract(address=checksum_address, abi=self.abi)
        self.function = self.contract.functions


    def printRed(self,str):
        print("\033[31m" + str +  "\033[0m")


    def textG(self,str):
        return "\033[32m" + str +  "\033[0m"


    def textR(self,str):
        return "\033[31m" + str + "\033[0m"

    def printN(self,str):
        print(self.NOTICE + str)


    def printW(self,str):
        print(self.WARNING + str)


    def printE(self,str):
        print(self.ERROR + str)


    def printO(self,str):
        print(self.OPERATING + str)


    def printS(self,str):
        print(self.SUCCESS + str)