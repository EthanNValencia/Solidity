from brownie import SimpleStorage, accounts, config

# brownie run scripts/read_value.py -- network rinkeby


def read_contract():
    simple_storage = SimpleStorage[-1]  # Brownie knows what the ABI and address is.
    print(simple_storage.retrieve())


def main():
    read_contract()


#                               <<< Brownie Console Example >>>
#  1. brownie console                                               -> Should start the shell.
#  2. SimpleStorage                                                 -> Should return an empty array.
#  3. account = accounts[0]                                         -> Should assign the account to the local blockchain.
#  4. account                                                       -> Should print the account number.
#  5. simple_storage = SimpleStorage.deploy({"from": account})      -> Should deploy the first smart contract to the local blockchain.
#  6. simple_storage                                                -> Should print the smart contract id.
#  7. SimpleStorage                                                 -> Should print the smart contract ids in the array.
#  8. len(SimpleStorage)                                            -> Should print 1.
#  9. simple_storage = SimpleStorage.deploy({"from": account})      -> Should deploy the second smart contract to the local blockchain.
# 10. len(SimpleStorage)                                            -> Should print 2.
# 11. simple_storage.retrieve()                                     -> Should print 5.
# 12. simple_storage.store(15, {"from":account})                    -> Should store 15.
# 13. simple_storage.retrieve()                                     -> Should print 15.
# 14. print("Hello")                                                -> Should print Hello.
# 15. quit()                                                        -> Should quit the shell.
