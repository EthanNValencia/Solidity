from scripts.helpful_scripts import (
    fund_with_link,
    get_account,
    get_contract,
    config,
    network,
)
from brownie import Lottery
import time


def deploy_lottery():
    # account = get_account(id="test-acount-name")  # Test this by placing brownie account id here
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )  # This will return the contract.
    print("Deploy lottery!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(
        1
    )  # Brownie gets confused if I don't wait for the last transaction to go through.
    print("The lottery has started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print("You have entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the recent winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
