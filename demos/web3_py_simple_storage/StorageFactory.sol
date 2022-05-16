// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;

import "./SimpleStorage.sol";

contract StorageFactory is SimpleStorage {

    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorageContract() public {
        SimpleStorage SimpleStorage = new SimpleStorage();
        simpleStorageArray.push(SimpleStorage);
    }

    /*
    Anytime you want to interact with a contract two things are necessary:
    1. Address
    2. ABI (application binary interface)
    */
    function sfStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber) public {
        SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).store(_simpleStorageNumber);
    }

    function sfGet(uint256 _simpleStorageIndex) public view returns(uint256) {
        return SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).retrieve();
    }
    
}