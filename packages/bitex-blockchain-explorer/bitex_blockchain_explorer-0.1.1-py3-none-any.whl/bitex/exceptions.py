class BlockchainExplorerException(Exception):
    """Base exception class for blockchain explorer errors."""
    pass


class APIRequestError(BlockchainExplorerException):
    """Exception raised for API request errors."""
    def __init__(self, status_code, message="API request error"):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)


class TransactionDetailsError(BlockchainExplorerException):
    """Exception raised for transaction details errors."""
    def __init__(self, message="Transaction details error"):
        self.message = message
        super().__init__(self.message)