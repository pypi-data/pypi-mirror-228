from typing import List

from metamask_institutional.sdk.adapters.cactus_create_tx_extra_params import CactusCreateTxExtraParams
from metamask_institutional.sdk.cactus.cactus_client import CactusClient
from metamask_institutional.sdk.cactus.cactus_get_transactions_params import CactusGetTransactionsParams
from metamask_institutional.sdk.cactus.cactus_transaction_detail import CactusTransactionDetail
from metamask_institutional.sdk.cactus.cactus_tx_params import CactusTXParams
from metamask_institutional.sdk.common.custodian import Custodian
from metamask_institutional.sdk.common.transaction import Transaction
from metamask_institutional.sdk.common.transaction_params import EIP1559TxParams
from metamask_institutional.sdk.common.transaction_params import LegacyTxParams
from metamask_institutional.sdk.utils.map_transaction_status import map_transaction_status


class CactusAdapter(Custodian):

    def __init__(self, client: CactusClient) -> None:
        self.client = client

    def get_transaction(self, transaction_id, chain_id=1) -> Transaction:
        params = CactusGetTransactionsParams(
            chainId=chain_id,
            transactionId=transaction_id,
        )
        cactus_transaction_details = self.client.get_transactions(params)

        result = cactus_transaction_details[0]
        return self.__map_cactus_transaction_to_transaction(result)

    def get_transactions(self, chain_id=1) -> List[Transaction]:
        params = CactusGetTransactionsParams(
            chainId=chain_id,
        )
        cactus_transaction_details = self.client.get_transactions(params)

        return list(map(lambda cactus_tx: self.__map_cactus_transaction_to_transaction(cactus_tx), cactus_transaction_details))

    def create_transaction(self, tx_params, extra_params) -> Transaction:
        # Parse and type check params
        type_ = tx_params["type"] if 'type' in tx_params else 1
        tx_params_parsed = EIP1559TxParams(**tx_params) if type_ == 2 else LegacyTxParams(**tx_params)
        extra_params_parsed = CactusCreateTxExtraParams(**extra_params)

        gasPrice = tx_params_parsed.gasPrice if type_ == 1 else None
        maxPriorityFeePerGas = tx_params_parsed.maxPriorityFeePerGas if type_ == 2 else None
        maxFeePerGas = tx_params_parsed.maxFeePerGas if type_ == 2 else None

        cactus_tx_params = CactusTXParams(
            from_=tx_params_parsed.from_,
            to=tx_params_parsed.to,
            gasLimit=tx_params_parsed.gas,
            value=tx_params_parsed.value,
            data=tx_params_parsed.data,
            gasPrice=gasPrice,
            maxPriorityFeePerGas=maxPriorityFeePerGas,
            maxFeePerGas=maxFeePerGas
        )
        cactus_transaction_detail = self.client.create_transaction(extra_params_parsed.chainId, cactus_tx_params)
        return self.__map_cactus_transaction_to_transaction(cactus_transaction_detail)

    def __map_cactus_transaction_to_transaction(self, cactus_transaction_detail: CactusTransactionDetail) -> Transaction:
        return Transaction(
            id=cactus_transaction_detail.custodian_transactionId,
            type="1" if cactus_transaction_detail.gasPrice is not None else "2",
            from_=cactus_transaction_detail.from_,
            to=None,
            value=None,  # TODO Why no field "value" on the response from Cactus API?
            gas=cactus_transaction_detail.gasLimit,
            gasPrice=cactus_transaction_detail.gasPrice,
            maxPriorityFeePerGas=cactus_transaction_detail.maxPriorityFeePerGas,
            maxFeePerGas=cactus_transaction_detail.maxFeePerGas,
            nonce=cactus_transaction_detail.nonce if cactus_transaction_detail.nonce != "" else None,
            data=None,  # TODO Why no field "data" on the response from Cactus API?
            hash=cactus_transaction_detail.transactionHash,
            status=map_transaction_status(cactus_transaction_detail.transactionStatus, "Unknown"),
        )
