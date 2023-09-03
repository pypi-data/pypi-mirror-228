from typing import Dict, Optional

import pytest

from profitpulse.account import Account
from profitpulse.account_name import AccountName
from profitpulse.application.open_account import (
    AccountAlreadyExistsError,
    OpenAccountService,
)


class AccountsStub:
    def __init__(self) -> None:
        self._accounts: Dict[str, Account] = dict()

    def get(self, account_name: str) -> Optional[Account]:
        try:
            return self._accounts[account_name]
        except KeyError:
            return None

    def __setitem__(self, account_name: str, account: Account):
        self._accounts[account_name] = account


class OpenAccountRequest:
    def __init__(self, account_name: str):
        self._account_name = AccountName(account_name)

    @property
    def account_name(self) -> AccountName:
        return self._account_name


def test_raise_error_if_an_account_with_same_name_already_exists():
    request = OpenAccountRequest(account_name="TheAccountName")
    accounts = AccountsStub()
    service = OpenAccountService(accounts)
    service.execute(request)

    with pytest.raises(AccountAlreadyExistsError) as excinfo:
        service.execute(request)

    assert str(excinfo.value) == "An account with the same name already exists"  # nosec


def test_save_account_when_its_a_new_account():
    request = OpenAccountRequest(account_name="TheAccountName")
    accounts = AccountsStub()
    service = OpenAccountService(accounts)

    service.execute(request)

    assert accounts.get(str(request.account_name)) is not None  # nosec
