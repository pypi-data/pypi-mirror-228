from dataclasses import dataclass


@dataclass(frozen=True)
class AccountName:
    name: str

    def __str__(self):
        return self.name
