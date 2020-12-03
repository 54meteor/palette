import sys
# import hashlib
from tokenContracts import TokenContracts
from bbcBillContracts import BbcBillContracts

bbcBranch = "000847ccaed396e138fbefa338a3e4c76622e3e228a52ed1b6c443cf84aff1bd"
bbcAddress = "1rvvarethz92rrgef7tamtfk9axb3gsxzd3pwkc93q1p6yazebdwr5mfd"
bbcTxid = "5fc61fbfc56ccb1120f297ce7e78c46af8e89f9e3820dff78f85034b67d4cbeb"


def main(argv):
    print("==============正常情况===============================")
    testInFlow(10000,1000)
    print("==============授权额度不足============================")
    testInFlow(100,10000)
    print("==============入账为零===============================")
    testInFlow(100,0)
    print("==============入账合约地址是零地址======================")
    testContractZero()
    print("==============正常退回操作=============================")
    testRetrace(900,100)
    print("==============合约余额不足=============================")
    testRetrace(900, 200)
    print("==============退回金额为零=============================")
    testRetrace(0, 200)
    print("==============退回合约为零=============================")
    testRetraceContract(600, 200)
    print("==============退回钱包为零=============================")
    testRetraceWallet(600, 200)
    print("==============正常流出操作=============================")
    testWithDraw(500,100)
    print("==============流出金额为零=============================")
    testRetrace(0, 200)
    print("==============流出合约为零=============================")
    testWithDrawContract(600, 200)
    print("==============流出钱包为零=============================")
    testWithDrawWallet(600, 200)
    print("==============修改管理员===============================")
    chageAdmin()
    print("==============非管理员操作退回==========================")
    adminRetraceNotAdmin(500,100)
    print("================管理员操作退回==========================")
    adminRetrace(500, 100)
    print("==============非管理员操作流出==========================")
    adminWithDrawNotAdmin(500, 100)
    print("================管理员操作流出==========================")
    adminWithDraw(500, 100)

def adminWithDrawNotAdmin(amount,fee):
    cts, bbc, hash, ownerBalance = testInFlow(10000, 1000)
    bbc.printN("defaultAccount is: " + str(bbc.getDefaultAccount()))
    bbc.testTransferAdmin(bbc.accountList[5])
    bbc.printN("defaultAccount is: " + str(bbc.getDefaultAccount()))
    bbc.printN("defaultAccount isAdmin: " + str(bbc.testAdmin()))
    bbc.testWithDraw(bbcTxid, bbcBranch,
                     cts.accountList[2], cts.contractAddr, amount, fee, 50)

def adminWithDraw(amount,fee):
    cts, bbc, hash, ownerBalance = testInFlow(10000, 1000)
    bbc.printN("defaultAccount is: " + str(bbc.getDefaultAccount()))
    bbc.testTransferAdmin(bbc.accountList[5])
    bbc.setDefaultAccount(bbc.accountList[5])
    bbc.printN("defaultAccount is: " + str(bbc.getDefaultAccount()))
    bbc.printN("defaultAccount isAdmin: " + str(bbc.testAdmin()))
    bbc.testWithDraw(bbcTxid, bbcBranch,
                     cts.accountList[2], cts.contractAddr, amount, fee, 50)

def adminRetraceNotAdmin(amount,fee):
    cts, bbc, hash, ownerBalance = testInFlow(10000, 1000)
    bbc.printN("defaultAccount is: " + str(bbc.getDefaultAccount()))
    bbc.testTransferAdmin(bbc.accountList[5])
    bbc.printN("defaultAccount is: " + str(bbc.getDefaultAccount()))
    bbc.printN("defaultAccount isAdmin: " + str(bbc.testAdmin()))
    bbc.testRetrace(hash, amount, cts.accountList[1], cts.contractAddr, fee)

def adminRetrace(amount,fee):
    cts, bbc, hash, ownerBalance = testInFlow(10000, 1000)
    bbc.printN("defaultAccount is: " + str(bbc.getDefaultAccount()))
    bbc.testTransferAdmin(bbc.accountList[5])
    bbc.setDefaultAccount(bbc.accountList[5])
    bbc.printN("defaultAccount is: " + str(bbc.getDefaultAccount()))
    bbc.printN("defaultAccount isAdmin: " + str(bbc.testAdmin()))
    bbc.testRetrace(hash, amount, cts.accountList[1], cts.contractAddr, fee)

def chageAdmin():
    (cts, bbc) = initContract()
    bbc.testTransferAdmin(bbc.accountList[5])

def testRetrace(amount,fee):
    cts,bbc,hash,ownerBalance = testInFlow(10000,1000)
    bbc.testRetrace(hash,amount,cts.accountList[1],cts.contractAddr,fee)
    balance = cts.testBalanceOf(bbc.contractAddr)
    outRs(cts,balance == 0)
    balance = cts.testBalanceOf(cts.accountList[1])
    outRs(cts,balance == amount)
    balance = cts.testBalanceOf(cts.accountList[0])
    outRs(cts,balance == ownerBalance - amount)

def testRetraceWallet(amount,fee):
    cts, bbc, hash, ownerBalance = testInFlow(10000, 1000)
    bbc.testRetrace(hash,amount,cts.ZERO,cts.contractAddr,fee)

def testRetraceContract(amount,fee):
    cts, bbc, hash, ownerBalance = testInFlow(10000, 1000)
    bbc.testRetrace(hash,amount,cts.accountList[1],cts.ZERO,fee)


def testInFlow(approve,amount):
    (cts, bbc) = initContract()
    cts.approve(bbc.contractAddr, approve)
    ownerBalance = cts.getOwnerBalance()
    hash = bbc.testInFlow(amount,cts.contractAddr,bbcBranch,bbcAddress)
    balance = cts.testBalanceOf(bbc.contractAddr)
    outRs(cts,balance == amount)
    balance = cts.testBalanceOf(cts.accountList[0])
    outRs(cts, balance == ownerBalance - amount)
    return (cts,bbc,hash,ownerBalance)

def testContractZero():
    (cts, bbc) = initContract()
    bbc.testInFlow(100, cts.ZERO, bbcBranch, bbcAddress)

def testWithDraw(amount,fee):
    cts,bbc,hash,ownerBalance = testInFlow(10000,1000)
    bbc.testWithDraw(bbcTxid,bbcBranch,
                     cts.accountList[2],cts.contractAddr,amount,fee,50)
    balance = cts.testBalanceOf(bbc.contractAddr)
    outRs(cts, balance == 1000 - amount - fee)
    balance = cts.testBalanceOf(cts.accountList[2])
    outRs(cts, balance == amount)
    balance = cts.testBalanceOf(cts.accountList[0])
    outRs(cts, balance == ownerBalance - amount - cts.testBalanceOf(bbc.contractAddr))

def testWithDrawWallet(amount,fee):
    cts, bbc, hash, ownerBalance = testInFlow(10000, 1000)
    bbc.testWithDraw(bbcTxid, bbcBranch,
                     cts.ZERO, cts.contractAddr, amount, fee, 50)

def testWithDrawContract(amount,fee):
    cts, bbc, hash, ownerBalance = testInFlow(10000, 1000)
    bbc.testWithDraw(bbcTxid, bbcBranch,
                     cts.accountList[2], cts.ZERO, amount, fee, 50)

def initContract():
    cts = TokenContracts("ArmorsToken", "ArmorsToken.sol");
    cts.deploy_contract()
    bbc = BbcBillContracts("BBCBill", "BBCBill_only_erc20.sol");
    bbc.deploy_contract()
    return (cts,bbc)

def outRs(cts,rs):
    if(rs):
        cts.printS("PASS")
    else:
        cts.printE("FAIL")



if __name__ == "__main__":
   main(sys.argv[1:])