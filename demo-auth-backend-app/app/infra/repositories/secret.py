from dataclasses import dataclass


@dataclass
class SecretRepository:
    value: str = "42"

    def get(self) -> str:
        return self.value

    def set(self, new_value):
        self.value = new_value
