from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)

# from web3 import Web3


def deploy_fund_me():
    account = get_account()

    # pass the price feed address to out fundme contract
    # PASS VARIABLE TO CONSTRUCTOR FUNCTION IN SOL.FILE

    # If we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks
    if (
        network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS
    ):  # a flexible way to identify local blockchain
        # live chain
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        # dev chain, in order to get local contract address
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
