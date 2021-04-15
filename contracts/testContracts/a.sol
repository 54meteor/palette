pragma solidity ^0.8.0;

// SPDX-License-Identifier: SimPL-2.0

contract A{

    string m;

    function getM() public view returns(string memory){
        return m;
    }
}