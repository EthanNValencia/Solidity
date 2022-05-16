// SPDX-License-Identifier: MIT
pragma solidity ^0.6.0;
// pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    // uint256 otherNumber; /// this will get initialized to 0
    uint256 favoriteNumber = 5;
    /*
    bool favoriteBool = true;
    string favoriteString = "String";
    int256 favoriteInt = -5;
    address favoriteAddress = 0x4772D446dc740bb8B6Cf0C8B544d14e4D26F7085;
    bytes32 favoriteByes = "cat"; /// 32 bytes is the max size but I can do less bytes. 
    */

    // Mutator function
    function store(uint256 _number) public returns(uint256){
        favoriteNumber = _number;
        return _number;
    }

    // The view keyword - reads off the blockchain
    // blue buttons are view functions
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }

    // pure functions are functions that do a purely mathematical operation
    function pureExample(uint256 number) public pure {
        number + number; // This isn't saved
    }

    People public person = People({favoriteNumber: 2, name: "Edward"});
    
    People[] public people; // This is a dynamic array.
    mapping(string => uint256) public nameToFavoriteNumber; 
    // People[1] public fixedArray; // This is a fixed array of length 1.

    struct People { // a struct is a type
        uint256 favoriteNumber; // index 0
        string name;  // index 1
    }

    // There are two ways to store data.
    // 1. memory - stores in memory, or during execution. 
    // 2. storage - it means the data will persist even after execution.
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People({favoriteNumber: _favoriteNumber, name: _name}));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

}