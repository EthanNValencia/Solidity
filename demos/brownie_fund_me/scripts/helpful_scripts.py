from brownie import network, MockV3Aggregator, config, accounts, FundMe
from web3 import Web3

# This method will provide the credentials for either a development network or a test network (whichever is being deployed to).
def get_account():
    if network.show_active() == "development":
        return accounts[0]  # Dev network account
    else:
        return accounts.add(config["wallets"]["from_key"])


# This method will fill the credentials for either a development network or a test network (whichever is being deployed to).
def get_verification(account):
    if network.show_active() == "development":  # This will deploy to ganache
        print(f"The active network is {network.show_active()}")
        print("Deploying Mocks...")
        mock_aggregator = MockV3Aggregator.deploy(
            18, Web3.toWei(2000, "ether"), {"from": account}
        )
        return FundMe.deploy(
            mock_aggregator.address,
            {"from": account},
            publish_source=get_verify(),
        )
    else:
        print(f"The active network is {network.show_active()}")
        print("Deploying to network...")
        return FundMe.deploy(
            config["networks"][network.show_active()]["eth_usd_price_feed"],
            {"from": account},
            publish_source=get_verify(),
        )


def get_verify():
    return config["networks"][network.show_active()].get("verify")
