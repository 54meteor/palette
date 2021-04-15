import sys

from tokenContracts import TokenContracts
from coveSwf import Coverswf



def main(argv):
    cts = TokenContracts("SeaweedToken","SeaweedToken.sol","0.6.12","/contracts/swf/")
    cts.deploy_contract_no_owner()
    cts.testBalanceOf(cts.getDefaultAccount())

    mint = TokenContracts("ERC20PresetMinterPauser", "ERC20PresetMinterPauser.sol", "0.6.12", "/contracts/swf/")
    mint.deploy_contract1("rSwf","RSWF")
    mint.testMint(cts.accountList[1],20 * 10 ** 18)

    cover = Coverswf("convetSWF","RSWFtoSWF.sol","0.6.12","/contracts/swf/")
    cover.deploy_contract_no_owner(cts.contractAddr,mint.contractAddr,10 ** 8)

    cts.testTransfer(cts.getDefaultAccount(), cover.contractAddr,5000 * 10 ** 18)
    cover.setDefaultAccount(cover.accountList[1])
    mint.setDefaultAccount(cover.accountList[1])
    mint.approve(cover.contractAddr,100 * 10 ** 18)
    mint.testBalanceOf(mint.accountList[1])
    cts.testBalanceOf(cts.accountList[1])

    cover.testCheckExchange(20 * 10 ** 18)
    cover.testGetAvailable()
    cover.testExchange(20 * 10 ** 18)
    mint.testBalanceOf(cts.accountList[1])
    cts.testBalanceOf(cts.accountList[1])

    # seaweed = SeaweedInital("SeaweedInitialOffering","SeaweedInitialOffering.sol","0.6.12")
    # seaweed.deploy_contract(cts.contractAddr)
    # seaweed.testInit(cts)
    # # tstMin(seaweed,cts)
    # tstMin_Max(seaweed,cts)
    # tstWithdraw(seaweed,cts)




if __name__ == "__main__":
   main(sys.argv[1:])