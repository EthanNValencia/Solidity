from brownie import Lottery, accounts, network, config, web3, exceptions
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account

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
    assert entrance_fee == expected_entrance_fee  # Assert


def test_cannot_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()
    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})
