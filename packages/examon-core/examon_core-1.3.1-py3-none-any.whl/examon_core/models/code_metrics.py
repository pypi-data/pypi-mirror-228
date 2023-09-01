from dataclasses import dataclass


@dataclass
class CodeMetrics:
    no_of_functions: int = None
    loc: int = None
    lloc: int = None
    sloc: int = None
    difficulty: float = None
    categorised_difficulty: str = None
    imports: list[str] = None

    def __repr__(self):
        return f'CodeMetrics(difficulty: {self.difficulty},' \
               f'no_of_functions: {self.no_of_functions}, ' \
               f'loc: {self.loc}, ' \
               f'lloc: {self.lloc}, ' \
               f'lloc: {self.sloc})'
