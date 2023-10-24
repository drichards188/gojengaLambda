import logging
from decimal import *
from opentelemetry import trace

from app.storage.Dynamo import Dynamo

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


class AccountHandler:
    @staticmethod
    def handle_get_account(username: str, is_test: bool) -> dict:
        # table_name: str = 'ledger'
        # if is_test:
        #     table_name = 'ledgerTest'

        table_name: str = 'ledgerTest'

        try:
            print(f'--> handle getting account {username}')
            user = Dynamo.get_item(table_name, {'name': username})
            return user
        except Exception as e:
            logger.info(f'error {e}')
            raise ValueError(e)

    @staticmethod
    def handle_create_account(username: str, balance: Decimal, is_test: bool) -> str:
        table_name: str = 'ledger'
        if is_test:
            table_name = 'ledgerTest'
        try:
            resp = Dynamo.create_item(table_name, {'name': username,
                                                   'balance': balance})
            return resp
        except Exception as e:
            logger.info(f'error {e}')
            raise ValueError(e)

    @staticmethod
    def handle_update_account(username: str, balance: Decimal, is_test: bool) -> str:
        table_name: str = 'ledger'
        if is_test:
            table_name = 'ledgerTest'
        try:
            resp = Dynamo.update_account_balance(table_name, {'name': username,
                                                              'balance': balance})
            return resp
        except Exception as e:
            logger.info(f'error {e}')
            raise ValueError(e)

    @staticmethod
    def handle_modify_account(username: str, balance: Decimal, is_test: bool) -> str:
        with tracer.start_as_current_span(
                "handle_modify_user",
                attributes={'attr.username': username, 'is_test': is_test}):
            table_name: str = 'ledger'
            if is_test:
                table_name = 'ledgerTest'
            try:
                current_balance = Dynamo.get_item(table_name, {'name': username})
                new_balance: float = current_balance["balance"] + balance

                resp = Dynamo.update_account_balance(table_name, {'name': username,
                                                                  'balance': new_balance})
                return resp
            except Exception as e:
                logger.info(f'error {e}')
                raise ValueError(e)

    @staticmethod
    def handle_delete_account(username: str, is_test: bool) -> str:
        with tracer.start_as_current_span(
                "handle_delete_account",
                attributes={'username': username, 'is_test': is_test}):
            table_name: str = 'ledger'
            if is_test:
                table_name = 'ledgerTest'
            try:
                resp = Dynamo.delete_item(table_name, {'name': username})

            except Exception as e:
                logger.info(f'error {e}')
                raise ValueError(e)

            if is_test:
                table_name = 'portfolioTest'
            else:
                table_name = 'portfolio'
            try:
                resp = Dynamo.delete_item(table_name, {'name': username})
            except Exception as e:
                logger.info(f'error {e}')
                raise ValueError(e)

            if is_test:
                table_name = 'usersTest'
            else:
                table_name = 'users'
            try:
                resp = Dynamo.delete_item(table_name, {'name': username})
            except Exception as e:
                logger.info(f'error {e}')
                raise ValueError(e)

            return resp

    @staticmethod
    def handle_transaction(sender: str, receiver: str, amount: Decimal, is_test: bool) -> str:
        with tracer.start_as_current_span(
                "handle_transaction",
                attributes={'attr.sender': sender, 'attr.receiver': receiver, 'is_test': is_test}):
            table_name: str = 'ledger'
            if is_test:
                table_name = 'ledgerTest'

            #     todo check usernames are valid before transaction
            try:
                ping_recipient = AccountHandler.handle_get_account(receiver, is_test)
                if "message" in ping_recipient and ping_recipient["message"] == 'item not found':
                    raise ValueError('recipient not found')

                sender_resp = AccountHandler.handle_modify_account(sender, amount * -1, is_test)
                if sender_resp == 'update item success':
                    receiver_resp = AccountHandler.handle_modify_account(receiver, amount, is_test)
                    if receiver_resp != 'update item success':
                        return 'transaction failed'
                else:
                    return 'transaction failed'

                return sender_resp
            except Exception as e:
                if sender_resp == 'update item success':
                    rollback_resp = AccountHandler.handle_modify_account(sender, amount, is_test)
                    if rollback_resp != 'update item success':
                        logger.info(f'failed to rollback transaction')
                logger.info(f'error {e}')
                raise ValueError(e)
