# Examples

## Listing supported custodians

```py
from metamask_institutional.sdk import CustodianFactory

# Instantiate the factory
factory = CustodianFactory()

supported_custodians = factory.get_supported_custodians()
print(supported_custodians)

# [ "qredo", "qredo-dev", "cactus", ... ]
```

## Instantiating a custodian

```py
from metamask_institutional.sdk import CustodianFactory

# Use the factory to instantiate a custodian. It figures out itself which API and parameters to use.
factory = CustodianFactory()
custodian2 = factory.create_for("qredo-dev", "YOUR-REFRESH-TOKEN-QREDO-DEV")
custodian3 = factory.create_for("cactus-dev", "YOUR-REFRESH-TOKEN-CACTUS-DEV")
```

## Creating a transaction

To run each of these examples, first export your custodian's token in the expected environment variable, then run the example file. For instance:

```bash
$ export MMISDK_TOKEN_BITGO_TEST=xxxx && python getting_a_transaction_bitgo.py
```

> Note: Each example file expects to find to token under a specific environment variable name, that depends on the custodian and the environment (dev/test/prod) you're addressing. Read each example's code to figure out the right variable.

### Qredo

<details>

```py
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
```

</details>

## Getting a transaction

To run each of these examples, first export your custodian's token in the expected environment variable, then run the example file. For instance:

```bash
$ export MMISDK_TOKEN_BITGO_TEST=xxxx && python getting_a_transaction_bitgo.py
```

> Note: Each example file expects to find to token under a specific environment variable name, that depends on the custodian and the environment (dev/test/prod) you're addressing. Read each example's code to figure out the right variable.

### Qredo

<details>

```py
import os

from metamask_institutional.sdk.factory.custodian_factory import CustodianFactory

# Instantiate the factory
factory = CustodianFactory()

# Grab your token from the environment, or anywhere else
token = os.environ["MMISDK_TOKEN_QREDO_DEV"]

custodian = factory.create_for("qredo-dev", token)

# Get the transaction
transaction = custodian.get_transaction("2ELvFICFt3RnXWdyxjkMvFN80xr")

print(type(transaction))
# <class 'metamask-institutional.sdk.common.transaction.Transaction'>

print(transaction)
# id='2ELvFICFt3RnXWdyxjkMvFN80xr'
# type='1'
# from_='0x62468FD916bF27A3b76d3de2e5280e53078e13E1'
# to='0x62468FD916bF27A3b76d3de2e5280e53078e13E1'
# value='1'
# gas='21000'
# gasPrice='1000'
# maxPriorityFeePerGas=None
# maxFeePerGas=None
# nonce='0'
# data=''
# hash=''
# status=TransactionStatus(finished=False, submitted=False, signed=False, success=False, displayText='Unknown', reason='Unknown')
```

</details>
