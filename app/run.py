import sys
import contracts




def main(argv):
    cts = contracts.Contracts("B","b.sol","0.8.0","/contracts/testContracts/")
    cts.deploy_contract1("a","b")
    print(cts.function.getM().call())
    print(cts.function.getN().call())



if __name__ == "__main__":
   main(sys.argv[1:])