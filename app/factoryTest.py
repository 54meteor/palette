import sys
from factoryContracts import FactoryContracts
from tokenContracts import TokenContracts
from routerContracts import RouterContracts



def main(argv):
    token = TokenContracts("ArmorsToken", "ArmorsToken.sol");

    token.deploy_contract()

    factory = FactoryContracts("UniswapV2Factory","factory.sol");

    factory.deploy_contract()

    router = RouterContracts("UniswapV2Router02","router.sol","0.6.6");

    router.deploy_contract(factory.contractAddr,token.contractAddr);

    # cts.getContractName()
    # cts.getOwnerBalance()
    # cts.testTransfer()
    # cts.testTransferZero()


if __name__ == "__main__":
   main(sys.argv[1:])