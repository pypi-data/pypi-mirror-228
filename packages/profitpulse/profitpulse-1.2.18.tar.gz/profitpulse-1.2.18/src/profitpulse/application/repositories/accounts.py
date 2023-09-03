from typing import Optional

from toolcat.database import text

from profitpulse.account import Account
from profitpulse.account_name import AccountName


class Accounts:
    """
    Accounts implement the AccountsRepository protocol.
    """

    def __init__(self, session):
        self._session = session

    def get(self, account_name: AccountName) -> Optional[Account]:
        sql_stmt = """
            SELECT account.name as name
              FROM account
             WHERE account.name = :name
        """
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(name=str(account_name))
        row = self._session.execute(prepared_statement).first()
        if not row:
            return None

        return Account(AccountName(row[0]))

    def __setitem__(self, _, account: Account):
        sql_stmt = """
            INSERT INTO account (name)
                 VALUES (:name)
        """
        prepared_statement = text(sql_stmt)
        prepared_statement = prepared_statement.bindparams(name=str(account.name))
        self._session.execute(prepared_statement)

    def __getitem__(self, key):
        self.get(key.name)
