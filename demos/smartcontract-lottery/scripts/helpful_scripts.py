from unicodedata import decimal
from brownie import network, accounts, config, MockV3Aggregator, Contract

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]

# This method will provide the credentials for either a development network or a test network (whichever is being deployed to).
def get_account(index=None, id=None):
    # Right now I use accounts[0], accounts.("env")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]  # Dev network account (local blockchain)
    return accounts.add(config["wallets"]["from_key"])  # This is default

    contract_to_mock = {"eth_usd_price_feed": MockV3Aggregator}
    """ 
    This contract will grab the contract address from the brownie config (if defined), otherweise,
    it will deploy a mock version of that contract, and return that mock contract. 
    Args: contract_name (string)
    Returns: brownie.network.contract.ProjectContract: The most recently deployed version of this contract. 
    """


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]  # MockV3Aggregator[-1]
    else:  #
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


DECIMALS = 8
INITIAL_VALUE = 200000000


def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    mock_price_feed = MockV3Aggregator.deploy(
        decimals, initial_value, {"from": account}
    )
    print("Deployed!")
