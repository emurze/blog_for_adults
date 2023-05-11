from dataclasses import dataclass, field
from typing import NoReturn

from ...modules.view.transform import Transform
from ...modules.exceptions import SetupDoesNotActivated


@dataclass(kw_only=True)
class View:
    """
    View for decorator.

    order: First - use setup() to put checks from @decorator(*checks).
           Second - use show() to print.
    """
    args: list[str] | str = field(kw_only=False)
    name: str
    time: float
    amount: int
    func_res: str
    is_changed: bool = field(default=False, repr=False)

    def setup(self, *, chk_result: bool, chk_arguments: bool) -> None:
        """1) Setup checks from @decorator(*checks)."""
        if not self.is_changed:
            self.is_changed = True
        self.func_res = f' -> {self.func_res}' if chk_result else ''
        self.args = ', '.join(self.args) if chk_arguments else ''

    def show(self) -> None | NoReturn:
        """2) Transform and print data."""
        if not self.is_changed:
            raise SetupDoesNotActivated
        print(f"[time - {Transform.get_time(self.time)}, "
              f"memory - {Transform.get_memory(self.amount)}]:  "
              f"{self.name}({self.args}){self.func_res}")
        return None  # for mypy
