import os

from metamask_institutional.sdk import CustodianFactory

# Instantiate the factory
factory = CustodianFactory()

# Grab your token from the environment, or anywhere else
token = os.environ["MMISDK_TOKEN_CACTUS_DEV"]

# Create the custodian, using the factory
custodian = factory.create_for("cactus-dev", token)

# Build tx details
tx_params = {
    "from": "0xFA42B2eCf59abD6d6BD4BF07021D870E2FC0eF20",
    "to": "0x7dc55e5C19c43FF6f027d0CeF656B2E1513916e6",
    "value": "100000000",  # in Wei
    "gas": "133997",
    "gasPrice": "200000000000",
}
cactus_extra_params = {
    "chainId": 5,  # Görli
    "note": "Some information"
}

# Create the tx from details and send it to the custodian
transaction = custodian.create_transaction(tx_params, cactus_extra_params)

print(type(transaction))
# <class 'metamask-institutional.sdk.common.transaction.Transaction'>

print(transaction)
# id='5CM05NCLMRD888888000800'
# type='1'
# from_='0xFA42B2eCf59abD6d6BD4BF07021D870E2FC0eF20'
# to=None
# value=None
# gas='133997'
# gasPrice='2774'
# maxPriorityFeePerGas=None
# maxFeePerGas=None
# nonce=''
# data=None
# hash=None
# status=TransactionStatus(finished=False, submitted=False, signed=False, success=False, displayText='Created', reason='Unknown')
