import requests

from .block import Block
from .transactions import Transaction, TransactionDetails
from .exceptions import APIRequestError

SEARCH_URL = 'https://www.blockchain.com/explorer/search'
TRANSACTIONS_URL = 'https://api.blockchain.info/haskoin-store/{chain}/address/{address}/{action}?limit={limit}&offset={offset}'

class Bitex:
    def __init__(self):
        self.session = requests.Session()


    def _handle_response(self, response):
        if response.status_code != 200:
            raise APIRequestError(response.status_code)

        return response.json()


    def search(self, address):
        try:
            response = self.session.post(SEARCH_URL, json={'search': address})

            return self._handle_response(response)

        except requests.RequestException as e:
            raise APIRequestError(message=f'API request error: {e}')


    def format_balance(self, balance):
        return balance / 100000000


    def balance(self, chain, address):
        try:
            url = TRANSACTIONS_URL.format(
                chain = chain, 
                address = address, 
                action = 'balance',
                limit = 0, 
                offset = 0
            )

            response = self.session.get(url)
        
            return self._handle_response(response)
        
        except requests.RequestException as e:
            raise APIRequestError(message=f'API request error: {e}')


    def transactions(self, chain, address, limit=20, offset=0):
        try:
            url = TRANSACTIONS_URL.format(
            	chain = chain, 
            	address = address, 
            	limit = limit, 
            	offset = offset,
                action = 'transactions'
            )
            
            response = self.session.get(url)
            transactions = self._handle_response(response)
            
            return [
            	Transaction(
                	txid           = transaction['txid'],
                	block_height   = transaction['block'].get('height'),
                	block_position = transaction['block'].get('position'),
                	mempool        = transaction['block'].get('mempol'),
            	) for transaction in transactions
            ]

        except requests.RequestException as e:
            raise APIRequestError(message=f'API request error: {e}')
