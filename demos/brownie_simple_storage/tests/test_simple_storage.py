from lib2to3.pgen2.literals import simple_escapes
from brownie import SimpleStorage, accounts

# brownie test              <- This runs the unit tests

# brownie networks list     <- This will list available test networks
# About Networks - Development Networks
# Development networks will not persist. They are temporary. (Ganache-CLI, Geth Dev, Hardhat, ...)
# About Networks - Ethereum Networks
# Ethereum networks will persist. (Rinkby, Kovan, Ropsten, ...)


def test_deploy():  # brownie test -k test_deploy
    # Arrange
    account = accounts[0]  # Get account
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})  # Get smart contract
    starting_value = simple_storage.retrieve()  # Retrieve value
    expected = 5  # Declare expected result
    # Assert
    assert starting_value == expected


def test_update_storage():  # brownie test -k test_update_storage
    # Arrange
    account = accounts[0]  # Get account
    # Act
    simple_storage = SimpleStorage.deploy({"from": account})  # Get smart contract
    expected = 15  # Declare expected result
    simple_storage.store(expected, {"from": account})
    # Assert
    assert simple_storage.retrieve() == expected


# Useful Commands
# brownie test --pdb    <- If a test fails this will open a python shell
# brown test -s         <- This will print more descriptive information
# https://docs.pytest.org/en/6.2.x/contents.html pytest has a lot of information about additional cmds
