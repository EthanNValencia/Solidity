from brownie import Lottery, accounts, network, config
from web3 import Web3

# 0.0022727272727273 (this is what the rate should be)


def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )
    assert lottery.getEntranceFee() > Web3.toWei(0.001, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.05, "ether")
