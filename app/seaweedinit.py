import sys

from tokenContracts import TokenContracts
from SeaweedInitialOffering import SeaweedInital



def main(argv):
    cts = TokenContracts("ArmorsToken","ArmorsToken.sol")
    cts.deploy_contract()

    seaweed = SeaweedInital("SeaweedInitialOffering","SeaweedInitialOffering.sol","0.6.12")
    seaweed.deploy_contract(cts.contractAddr)
    seaweed.testInit(cts)
    # tstMin(seaweed,cts)
    tstMin_Max(seaweed,cts)
    # tstWithdraw(seaweed,cts)

def tstMin(seaweed,cts):
    seaweed.testRW(1, cts.accountList[1])
    seaweed.testClaim(cts, cts.accountList[1])

def tstMin_Max(seaweed,cts):
    seaweed.testRW(1, cts.accountList[1])
    seaweed.testRW(2, cts.accountList[1])
    seaweed.testRW(2, cts.accountList[2])
    # seaweed.testRW(3, cts.accountList[3])
    # seaweed.testRW(4, cts.accountList[4])
    # seaweed.testRW(5, cts.accountList[5])
    seaweed.testClaim(cts, cts.accountList[1])
    seaweed.testClaim(cts, cts.accountList[2])
    # seaweed.testClaim(cts, cts.accountList[3])
    # seaweed.testClaim(cts, cts.accountList[4])
    # seaweed.testClaim(cts, cts.accountList[5])

def tstWithdraw(seaweed,cts):
    seaweed.testWithdrawProvidedHT()
    seaweed.testWithdrawUnclaimedSWF(cts)


if __name__ == "__main__":
   main(sys.argv[1:])