from brownie import accounts, config, SimpleStorage


def deploy_simple_storage():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    print(simple_storage)
    # account = accounts.load("ethannephew-test-account")
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)


def main():
    deploy_simple_storage()
