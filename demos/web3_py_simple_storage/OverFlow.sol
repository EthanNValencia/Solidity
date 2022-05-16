pragma solidity ^0.6.0;

contract OverFlow {

    /*
    In solidity numbers can wrap around their limit. So for example, the 
    maximum value that can be stored in uint8 is 255. 255 + 1 is 0, because
    it will wrap around to 0. Similarly, 255 + 100 is 99. 
    */
    function overflow() public pure returns (uint8) {
        uint8 big = 255 + uint8(1); // this will equal 0
        // big = 255 + uint8(100); // this will equal 99
        return big;
    }
    
}