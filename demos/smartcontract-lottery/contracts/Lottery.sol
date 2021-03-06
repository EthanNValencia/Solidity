// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    uint256 public usdEntryFee;
    uint256 public randomness; // Recent random number
    AggregatorV3Interface internal ethUsdPriceFeed;
    address payable public recentWinner; // Address of recent winner.
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyHash;

    // Notes on Constructors
    /* Constructors in Solidity are like initialization methods. They are only called when the contract is deployed to the blockchain.
     * Constructors should probably be public (generally). Making a constructor internal can be useful because it can then be called by
     * another contract within the same file.
     */
    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyHash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        // Implementing inherited constructor.
        usdEntryFee = 5 * (10**18); // Entry rate is $5
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyHash = _keyHash;
    }

    function enter() public payable {
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "Lottery state is not open."
        );
        require(msg.value >= getEntranceFee(), "Not enough Ethereum.");
        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        // It would probably be good to use safe math functions.
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; // 18 decimals
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Failed to start a new lottery."
        ); // The lottery cannot start if it is not closed.
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyHash, fee);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "The contract is not in the correct state."
        );
        require(_randomness > 0, "Random variable was not found.");
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);
        // Reset Lottery
        players = new address payable[](0);
        randomness = _randomness;
        lottery_state = LOTTERY_STATE.CLOSED;
    }
}
