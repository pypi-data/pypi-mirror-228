from profitpulse.account_name import AccountName


class Account:
    def __init__(self, account_name: AccountName):
        self._account_name = account_name

    @property
    def name(self) -> AccountName:
        return self._account_name
