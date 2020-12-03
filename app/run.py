import sys
import contracts




def main(argv):
    cts = contracts.Contracts("ESP","ArmorsToken.sol");
    cts.deploy_contract()
    print(cts.getContractName())
    cts.testTransfer()


if __name__ == "__main__":
   main(sys.argv[1:])