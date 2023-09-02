import os

from metamask_institutional.sdk import CustodianFactory

# Instantiate the factory
factory = CustodianFactory()

# Grab your token from an environment variable, or anywhere else
token = os.environ["MMISDK_TOKEN_BITGO_TEST"]

# Create the custodian, using the factory
custodian = factory.create_for("bitgo-test", token)

# Get the transaction
transaction = custodian.get_transaction("0a4a244b-dbd4-4a4a-bc3d-0cf8f2f5f618")

print(type(transaction))
# <class 'metamask-institutional.sdk.common.transaction.Transaction'>

print(transaction)
# id='0a4a244b-dbd4-4a4a-bc3d-0cf8f2f5f618'
# type='1'
# from_='0xeddb59689e4ec3931b8d42d615c0d4a7a3a208e7'
# to='0xb22505ee2aac7d52d4a218f5877cdbae3bbeec75'
# value='999000000'
# gas='300000'
# gasPrice=None
# maxPriorityFeePerGas=None
# maxFeePerGas=None
# nonce=None
# data='0x1111111111111111'
# hash=None
# status=TransactionStatus(finished=False, submitted=False, signed=False, success=False, displayText='Created', reason='Unknown')
