import pytest

from profitpulse.application.views.accounts import AccountsView
from testrig.scenario import DatabaseScenario


@pytest.mark.integration
def test_return_no_data_when_no_accounts(tmp_db_session):
    assert AccountsView(tmp_db_session).data == []  # nosec


@pytest.mark.integration
def test_return_one_account_when_one_account(tmp_db_session):
    DatabaseScenario(tmp_db_session).open_account(name="TheAccountName")

    assert AccountsView(tmp_db_session).data == [{"name": "TheAccountName"}]  # nosec
