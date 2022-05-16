from brownie import accounts, config, SimpleStorage


def deploy_simple_storage():
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    print(simple_storage)
    stored_value = simple_storage.retrieve()
    print(stored_value)
    transaction = simple_storage.store(
        15, {"from": account}  # Changes value to 15
    )  # Since this is a transaction, it is necessary to include who'll transact from.
    transaction.wait(1)  # wait for blockchain
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)  # This should print 15
    # account = accounts.load("ethannephew-test-account")
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)


def main():
    deploy_simple_storage()
