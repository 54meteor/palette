import sys

from tokenContracts import TokenContracts
from airdropContracts import Airdrop



def main(argv):
    cts = TokenContracts("ArmorsToken","ArmorsToken.sol")
    cts.deploy_contract()

    seaweed = Airdrop("TokenBatchTransfer","airdrop.sol","0.4.24")
    seaweed.deploy_contract(cts.contractAddr)
    tstInit(seaweed,cts)
    tstMax(seaweed,cts)
    cts.testBalanceOf("0xFc03756d9C89427dE703d3c9E27e80d8090B149A")
    cts.testBalanceOf("0x33226cF941867F49e87a9fcbB0325833f771CC9F")
    cts.testBalanceOf("0x99988439043709F21f6dd017d101d0162CDe7B3d")
    cts.testBalanceOf("0xF7993e93bFf57217650D3A12F6f7f5E687fA0083")
    cts.testBalanceOf("0xa0C4fA727267c81Ea31EeEF566eE8848E556155b")
    cts.testBalanceOf("0xC09FAAe04cA3796BdaBFe8A3582FA69e9243c657")

def tstInit(seaweed,cts):
    seaweed.testInit(cts)

def tstMin(seaweed,cts):
    seaweed.testSafeTransfer(seaweed.accountList[1],10000000,cts)

def tstMax(seaweed,cts):
    tos = ["0xFc03756d9C89427dE703d3c9E27e80d8090B149A","0x33226cF941867F49e87a9fcbB0325833f771CC9F","0x99988439043709F21f6dd017d101d0162CDe7B3d","0xF7993e93bFf57217650D3A12F6f7f5E687fA0083","0xa0C4fA727267c81Ea31EeEF566eE8848E556155b","0xC09FAAe04cA3796BdaBFe8A3582FA69e9243c657"]
    amounts = [95035201560000000000000,4000000000000000000000,4000000000000000000000,1644320243100000000000000,1783976513040000000000000,2000000000000000000000]
    seaweed.testBatchTransfer(tos,amounts,cts)



if __name__ == "__main__":
   main(sys.argv[1:])