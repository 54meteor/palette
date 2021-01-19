import sys
# import hashlib
from tokenContracts import TokenContracts
from bbcExchangeContracts import BbcExchangeContracts

bbcBranch = "000847ccaed396e138fbefa338a3e4c76622e3e228a52ed1b6c443cf84aff1bd"
bbcAddress = "1rvvarethz92rrgef7tamtfk9axb3gsxzd3pwkc93q1p6yazebdwr5mfd"
bbcTxid = "5fc61fbfc56ccb1120f297ce7e78c46af8e89f9e3820dff78f85034b67d4cbeb"
betweenPrimaryKey = "5fc61f96b2d292db5de7da197560316d44acf20372da1d783e57e1811e123953"
randI = "000847ca96d8f385f47dfde25c81ed17360f73f78dd7e0f6331c3b233e24fdd0"
randJ = "000847c6d06874ed25ebd28b927233a6200637516c150e871993d2fac777a0bd"
randKey = "1rvvarethz92rrgef7tamtfk9axb3gsxzd3pwkc93q1p6yazebdwr5mfd"

def main(argv):
    testNoBetween()
    testHasBetween()


def testNoBetween():
    approve = 10000
    amount = 100
    (cts, bbc) = initContract()
    cts.approve(bbc.contractAddr, approve)
    ownerBalance = cts.getOwnerBalance()
    bbc.testCreateOrder(cts.contractAddr, amount, bbcAddress, amount, 100,
                        cts.accountList[1], bbcAddress, 100, bbcBranch, bbcTxid)
    balance = cts.testBalanceOf(bbc.contractAddr)
    outRs(cts, balance == amount)
    balance = cts.testBalanceOf(cts.accountList[0])
    outRs(cts, balance == ownerBalance - amount)
    amount = bbc.testGetOrderTradePairAmount(bbc.getDefaultAccount(),bbcTxid)
    cts.printO(str(amount))
    return (cts, bbc, hash, ownerBalance)

def testHasBetween():
    approve = 10000
    amount = 1000
    (cts, bbc) = initContract()
    orderAddress = cts.accountList[0]
    betweenAddress = cts.accountList[1]
    buyAddress = cts.accountList[2]
    carryAddress = cts.accountList[3]
    cts.approve(bbc.contractAddr, approve)
    ownerBalance = cts.getOwnerBalance()
    bbc.testCreateOrder(cts.contractAddr, amount, bbcAddress, amount, 100,
                        cts.accountList[1], bbcAddress, 200, bbcBranch, bbcTxid)
    balance = cts.testBalanceOf(bbc.contractAddr)
    outRs(cts, balance == amount)
    bbc.setDefaultAccount(betweenAddress)
    balance = cts.testBalanceOf(cts.accountList[0])
    outRs(cts, balance == ownerBalance - amount)
    bbc.testGoBetween(orderAddress,cts.contractAddr,
            500,bbcAddress,400,buyAddress,
            carryAddress,randI,randJ,randKey,bbcTxid,betweenPrimaryKey)
    bbc.setDefaultAccount(orderAddress)
    amount = bbc.testGetOrderTradePairAmount(bbc.accountList[1],bbcTxid)
    cts.printO(str(amount))
    return (cts, bbc, hash, ownerBalance)





def initContract():
    cts = TokenContracts("ArmorsToken", "ArmorsToken.sol");
    cts.deploy_contract()
    bbc = BbcExchangeContracts("BBCExchange", "BBCExchange_amount.sol");
    bbc.deploy_contract()
    return (cts,bbc)

def outRs(cts,rs):
    if(rs):
        cts.printS("PASS")
    else:
        cts.printE("FAIL")



if __name__ == "__main__":
   main(sys.argv[1:])