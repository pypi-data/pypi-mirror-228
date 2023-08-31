import requests

from .block import Block
from .exceptions import TransactionDetailsError, APIRequestError

class TransactionDetails:
    def __init__(self, dictionary):
        self.dictionary = dictionary

        for key, value in dictionary.items():
            setattr(self, key, value)


    def __repr__(self):
        return f'<TransactionDetails: {self.txid}>'


    def keys(self):
        return self.dictionary.keys()


    def get(self):
        return self.dictionary


class Transaction:
    def __init__(self, txid, block_height, block_position, mempool=None):
        self.txid = txid
        self.block = Block(block_height, block_position)
        self.details_url = f'https://api.blockchain.info/haskoin-store/btc/transactions?txids={self.txid}'


    def _handle_response(self, response):
        if response.status_code != 200:
            raise APIRequestError(response.status_code)

        return response.json()


    def details(self):
        try:
            response = requests.get(self.details_url)
            data = self._handle_response(response)

            return TransactionDetails(data[0])

        except requests.RequestException as e:
            raise TransactionDetailsException(f'Failed to fetch transaction details: {e}')

    def __repr__(self):
        return f'<Transaction: {self.txid}>'
