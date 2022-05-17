from brownie import FundMe
from scripts.helpful_scripts import (
    get_account,
    get_verification,
)  # importing the get_account function from helpful_scripts

# brownie run scripts/deploy.py --network rinkeby


def deploy_fund_me():
    account = get_account()
    # 0x8A753747A1Fa494EC906cE90E9f37563A8AF630e

    fund_me = get_verification(account)
    return fund_me
    # print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
