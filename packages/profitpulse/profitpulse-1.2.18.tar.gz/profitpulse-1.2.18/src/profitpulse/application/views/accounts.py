from toolcat.database import text

from profitpulse.application.views.views import View


class AccountsView(View):
    def __init__(self, session) -> None:
        self._session = session

    @property
    def data(self):
        sql_stmt = "SELECT account.name as name FROM account"
        rows = self._session.execute(text(sql_stmt))

        return [{"name": row[0]} for row in rows]
