from dataclasses import dataclass


@dataclass
class Fee:
    code: str
    amount: int
    description: str = ''

    def __init__(self, code, amount, description):
        self.code = code
        self.amount = amount
        self.description = description

    def get_description_for_trademark(self, number):
        return f"{self.code}. {self.description} Свидетельство N{number}. НДС не облагается."

    def get_description_for_patent(self, number):
        return f"{self.code}. {self.description} Патент N{number}. НДС не облагается."
