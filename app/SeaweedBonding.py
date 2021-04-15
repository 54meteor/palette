import sys
import time

from tokenContracts import TokenContracts
from  SeaweedBondingContracts import SeaweedBonding



def main(argv):
    cts = TokenContracts("ArmorsToken","ArmorsToken.sol")
    cts.deploy_contract()

    seaweed = SeaweedBonding("LinearBondingCurve","LinearBondingCurve.sol","0.6.12")
    seaweed.deploy_contract(cts.contractAddr,6250008300,356600000000000)
    cts.testTransfer(cts.getDefaultAccount(),seaweed.contractAddr,40000000 * 10**18)

    cts.setDefaultAccount(cts.accountList[1])
    seaweed.setDefaultAccount(cts.accountList[1])

    ethAmount = seaweed.testCheckBuy(1000)
    seaweed.testBuy(cts,1000,ethAmount)
    ethAmount = seaweed.testCheckBuy(2000)
    seaweed.testBuy(cts,2000,ethAmount)

    cts.testBalanceOf(cts.getDefaultAccount())

    seaweed.testGetAvailable()
    cts.approve(seaweed.contractAddr, 1000 * cts.DECIMAL)
    seaweed.testCheckSell(299)

    seaweed.testSell(cts,299)
    print("pause 10 sec")
    time.sleep(15)
    print("resume")
    seaweed.testSell(cts,100)
if __name__ == "__main__":
   main(sys.argv[1:])
