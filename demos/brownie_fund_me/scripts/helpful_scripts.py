from brownie import network, MockV3Aggregator, config, accounts, FundMe

# from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200000000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork"]

# This method will provide the credentials for either a development network or a test network (whichever is being deployed to).
def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]  # Dev network account
    else:
        return accounts.add(config["wallets"]["from_key"])


# This method will fill the credentials for either a development network or a test network (whichever is being deployed to).
def get_verification(account):
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
    ):  # This will deploy to ganache
        deploy_mocks(account)
        return FundMe.deploy(
            MockV3Aggregator[-1].address,
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


# Web3.toWei(STARTING_PRICE, "ether")
def deploy_mocks(account):
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": account})
    print("Mocks have been deployed.")


# Adding Network Command
# brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork='https://eth-mainnet.alchemyapi.io/v2/LC7fmyaJmeszNiDMTG4rPfIG9BTYM1m2' accounts=10 mnemonic=brownie port=8545
