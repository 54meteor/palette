import sys
from factoryContracts import FactoryContracts




def main(argv):
    cts = FactoryContracts("UniswapV2Router02","router.sol");

    cts.deploy_contract()
    # cts.getContractName()
    # cts.getOwnerBalance()
    # cts.testTransfer()
    # cts.testTransferZero()


if __name__ == "__main__":
   main(sys.argv[1:])