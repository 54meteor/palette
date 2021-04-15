import sys
from factoryContracts import FactoryContracts
from tokenContracts import TokenContracts
from routerContracts import RouterContracts



def main(argv):
    token = TokenContracts("ArmorsToken", "ArmorsToken.sol");

    token.deploy_contract()

    factory = FactoryContracts("UniswapV2Factory","factory.sol");

    factory.deploy_contract()

    weth = TokenContracts("WETH9", "WETH9.sol")
    weth.deploy_contract_no_owner()

    router = RouterContracts("UniswapV2Router02","router.sol","0.6.6")

    router.deploy_contract(factory.contractAddr,weth.contractAddr)

    # 创建交易对
    factory.createPair(token.contractAddr,weth.contractAddr)
    # 查看交易对hash
    print(factory.getPair(token.contractAddr,weth.contractAddr))



    # cts.getContractName()
    # cts.getOwnerBalance()
    # cts.testTransfer()
    # cts.testTransferZero()


if __name__ == "__main__":
   main(sys.argv[1:])