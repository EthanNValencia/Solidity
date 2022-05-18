from scripts.helpful_scripts import get_account, get_contract


def deploy_lottery():
    # account = get_account(id="test-acount-name")  # Test this by placing brownie account id here
    account = get_account()
    lottery = Lottery.deploy(get_contract())


def main():
    deploy_lottery()
