"""
Cli adapters bridge the CLI with the application use cases.
"""

from pathlib import Path

from toolcat.database import Database, Session

from profitpulse.account_name import AccountName
from profitpulse.application.import_transactions import ServiceImportTransactions
from profitpulse.application.open_account import OpenAccountService
from profitpulse.application.repositories.accounts import Accounts
from profitpulse.application.repositories.transactions import Transactions
from profitpulse.application.views.accounts import AccountsView
from profitpulse.application.views.transactions import ViewTransactions
from profitpulse.infrastructure.gateway_cgd_file import GatewayCGDFile

database_path = Path.home() / Path("Library/Application Support/Profitpulse")


def report(seller, since, on):
    with Session(Database(database_path).engine) as session:
        view = ViewTransactions(session, seller, since, on)

    transactions, total = view.data
    if not seller:
        if not transactions:
            print("Could not find any transactions!")
            return

        for t in transactions:
            print(f"Description: '{t['description']:>22}', Value: {t['value']:>10}")
        return

    print(f"Description: '{seller}', Value: {round(total, 2)}")


def migrate_database():
    d = Database(database_path, Path("migrations/0001 - Initial.sql"))
    d.run_sql_file(Path("migrations/0002 - accounts.sql"))


def reset():
    db = Database(database_path)
    db.remove()


def import_file(file_path: Path):
    with Session(Database(database_path).engine) as session:
        gateway_cgd = GatewayCGDFile(file_path)
        transactions = Transactions(session)
        ServiceImportTransactions(gateway_cgd, transactions).execute()
        session.commit()


def show_accounts(printer):
    with Session(Database(database_path).engine) as session:
        for i in AccountsView(session).data:
            printer(i["name"])
        else:
            print("No accounts found")


class OpenAccountRequest:
    def __init__(self, name):
        self._name = AccountName(name)

    @property
    def account_name(self):
        return self._name


def open_account(name):
    with Session(Database(database_path).engine) as session:
        accounts = Accounts(session)
        request = OpenAccountRequest(name)
        OpenAccountService(accounts).execute(request)
        session.commit()
