import sys
from tokenContracts import TokenContracts


def main(argv):
    test = TokenContracts("SMN1", "DRF.sol")

    test.deploy_contract()
    test.testTransfer(test.getDefaultAccount(),test.accountList[1],1000 * test.DECIMAL)


    test.getContractName()
    test.getOwnerBalance()
    # test.testTransfer(test.getDefaultAccount(),test.accountList[1],1000 * test.DECIMAL)
    test.testTransferZero()


if __name__ == "__main__":
   main(sys.argv[1:])