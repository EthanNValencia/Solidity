from brownie import network, MockV3Aggregator, config, accounts, FundMe

# This method will provide the credentials for either a development network or a test network (whichever is being deployed to).
def get_account():
    if network.show_active() == "development":
        return accounts[0]  # Dev network account
    else:
        return accounts.add(config["wallets"]["from_key"])


# This method will fill the credentials for either a development network or a test network (whichever is being deployed to).
def get_verification(account):
    if network.show_active() == "development":
        print(f"The active network is {network.show_active()}")
        print("Deploying Mocks...")
        mock_aggregator = MockV3Aggregator.deploy(
            18, 200000000000000, {"from": account}
        )
        return FundMe.deploy(mock_aggregator.address, {"from": account})
    else:
        return FundMe.deploy(
            config["networks"][network.show_active()]["eth_usd_price_feed"],
            {"from": account},
            publish_source=True,
        )
