pragma solidity ^0.8.0;

// SPDX-License-Identifier: SimPL-2.0

import "./a.sol";

contract B is A{
    string n;

     constructor(string memory _m, string memory _n) {
         m = _m;
         n = _n;
     }

    function getN() public view returns(string memory){
        return n;
    }
}