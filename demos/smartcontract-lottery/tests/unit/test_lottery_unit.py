from brownie import Lottery, accounts, network, config, web3
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest

from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS

# 0.0022727272727273 (this is what the rate should be)


def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()  # Arrange
    entrance_fee = lottery.getEntranceFee()  # Act
    print(lottery.getEntranceFee())
    # If 2,000 eth / usd
    # usdEntryFee is 5
    # 2000 / 1 == 5/x == 0.0025
    expected_entrance_fee = Web3.toWei(2.5, "ether")  # Act
    assert entrance_fee == expected_entrance_fee
