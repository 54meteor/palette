import sys
from tokenContracts import TokenContracts




def main(argv):
    cts = TokenContracts("ArmorsToken","ArmorsToken.sol");

    cts.deploy_contract()
    cts.getContractName()
    cts.getOwnerBalance()
    cts.testTransfer()
    cts.testTransferZero()


if __name__ == "__main__":
   main(sys.argv[1:])