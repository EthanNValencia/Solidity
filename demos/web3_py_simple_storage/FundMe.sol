// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
/*
Interfaces compile down to the application binary interface (ABI). Anytime
I want to interact with a deployed smart contract I will need the ABI. I 
always need an ABI to interact with a contract.  
*/
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";


contract FundMe {

    using SafeMathChainlink for uint256; // This makes it so I do not have to worry about number wrapping. 
    // SafeMath will handle integer overflows. 
    mapping(address => uint256) public addressToAmountFunded; 
    address[] public funders; 
    address public owner;

    constructor() public { // This constructor runs when it is deployed to the blockchain. 
        owner = msg.sender; // This refers to the person who deploys the contract. 
        /* 
        When I deploy this contract, the owner of the contract will be
        my wallet. So the wallet of who deploys this will be the owner 
        of the contract when it is deployed to the blockchain. 
        */
    }

    function fund() public payable {
        uint256 minimumUSD = 10 * 10 ** 18; // It will have 18 decimals.
        require(getConversionRate(msg.value) >= minimumUSD, "You need to spend more ETH."); // If there isn't $50+ in Ether this will stop the method. This will revert the transaction. 
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        return priceFeed.version();
    }

/*
    (
      uint80 roundId,
      int256 answer,
      uint256 startedAt,
      uint256 updatedAt,
      uint80 answeredInRound
    );
    
    This ^ cleans up to this: 
    (,int256 answer,,,)

    So solidity needs to know what the variable places are but if the variables
    are not used they do not need to be declared. 
*/
    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e);
        (,int256 answer,,,) = priceFeed.latestRoundData();

        return uint256(answer * 10000000000); 
        // 293044783403 (it has 8 decimals)
        // 2930.44783403
    }

    function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    modifier onlyOwner {
        require(msg.sender == owner); 
        // The sender must be equal to the owner (the person who deployed).
        _; // This represents running the rest of the code. 
    }

    function withdraw() payable onlyOwner public { // onlyOwner modifier
        msg.sender.transfer(address(this).balance); // address of this contract
        for(uint256 funderIndex = 0; funderIndex < funders.length; funderIndex++) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }
        delete funders;
        //funders = new address[](0);
    }

}