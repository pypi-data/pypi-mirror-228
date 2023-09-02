import os

from metamask_institutional.sdk import CustodianFactory

# Instantiate the factory
factory = CustodianFactory()

# Grab your token from the environment, or anywhere else
token = os.environ["MMISDK_TOKEN_QREDO_DEV"]

# Create the custodian, using the factory
custodian = factory.create_for("qredo-dev", token)

# Build tx details
tx_params = {
    "from": "0x62468FD916bF27A3b76d3de2e5280e53078e13E1",
    "to": "0x62468FD916bF27A3b76d3de2e5280e53078e13E1",
    "value": "100000000000000000",  # in Wei
    "gas": "21000",
    "gasPrice": "1000",
    # "data": "0xsomething",
    # "type": "2"
    # "maxPriorityFeePerGas": "12321321",
    # "maxFeePerGas": "12321321",
}
qredo_extra_params = {
    "chainID": "3",
}

# Create the tx from details and send it to the custodian
transaction = custodian.create_transaction(tx_params, qredo_extra_params)
print(type(transaction))
# <class 'metamask-institutional.sdk.common.transaction.Transaction'>

print(transaction)
# id='2EzDJkLVIjmH6LZQ2W1T4wPcTtK'
# type='1'
# from_='0x62468FD916bF27A3b76d3de2e5280e53078e13E1'
# to='0x62468FD916bF27A3b76d3de2e5280e53078e13E1'
# value='100000000000000000'
# gas='21000'
# gasPrice='1000'
# maxPriorityFeePerGas=None
# maxFeePerGas=None
# nonce='0'
# data=''
# hash=''
# status=TransactionStatus(finished=False, submitted=False, signed=False, success=False, displayText='Created', reason='Unknown')
