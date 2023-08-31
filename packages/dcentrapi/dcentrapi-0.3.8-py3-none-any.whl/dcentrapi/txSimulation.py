from typing import List
from dcentrapi.Base import Base
from dcentrapi.requests_dappi import requests_post

SIM_TYPE_QUICK = 'quick'
SIM_TYPE_ABI = 'abi'
SIM_TYPE_FULL = 'full'


# See: https://docs.tenderly.co/simulations-and-forks/intro-to-simulations
class TxSimulation(Base):

    # Format of tx:
    # tx = {
    #     "from": "0x1234",
    #     "to": "0x5678",
    #     "input": "0x12345678000000...data",
    # }
    # Optional parameters:
    # "gas": 1234567,
    # "gas_price": 0,
    # "value": 100,
    # "state_objects": (see Tenderly documentation for overwriting state)

    # See: https://docs.tenderly.co/simulations-and-forks/simulation-api/using-simulation-api
    def simulate_transaction_single(
        self,
        tx: dict,
        network_id: int,  # chain-id
        simulation_type: str = SIM_TYPE_FULL,  # quick, abi, or full
    ):
        url = self.url + "simulate_transactions"
        data = {
            "simulation_type": simulation_type,
            "network_id": network_id,
            "tx_single": tx,
        }
        response = requests_post(url, json=data, headers=self.headers)
        return response.json()

    # Format of tx_bundle is [tx0, tx1, tx2...]
    # See: https://docs.tenderly.co/simulations-and-forks/simulation-api/simulation-bundles
    def simulate_transaction_bundle(
        self,
        tx_bundle: List[dict],
        network_id: int,
        simulation_type: str = SIM_TYPE_FULL,
    ):
        url = self.url + "simulate_transactions"
        data = {
            "simulation_type": simulation_type,
            "network_id": network_id,
            "tx_bundle": tx_bundle,
        }
        response = requests_post(url, json=data, headers=self.headers)
        return response.json()
