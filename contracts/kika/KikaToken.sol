pragma solidity 0.6.6;

import "@openzeppelin/contracts/GSN/Context.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/math/SafeMath.sol";
import "@openzeppelin/contracts/utils/Address.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract KikaToken is ERC20("KIKA", "KIKA"), Ownable {
    uint256 public MAX_TOTAL_SUPPLY  = 1e27;
     constructor () public {
        _setupDecimals(18);
    }

    function mint(address _to, uint256 _amount) public onlyOwner {
        uint256 totalSupply  =  totalSupply();
        if(totalSupply ==  MAX_TOTAL_SUPPLY){
            return;
        }
        if(totalSupply.add(_amount) <= MAX_TOTAL_SUPPLY){
            _mint(_to, _amount);
        }                
        else{
            uint256 amount = MAX_TOTAL_SUPPLY.sub(totalSupply);
            _mint(_to, amount);
        }
    }
}
