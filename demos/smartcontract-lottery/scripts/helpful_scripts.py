from brownie import network, accounts, config

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

    """ 
    This contract will grab the contract address from the brownie config (if defined), otherweise,
    it will deploy a mock version of that contract, and return that mock contract. 
    Args: contract_name (string)
    Returns: brownie.network.contract.ProjectContract: The most recently deployed version of this contract. 
    """


def get_contract(contract_name):
    pass
