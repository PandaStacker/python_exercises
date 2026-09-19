from __future__ import annotations

from io import StringIO
import unittest
from unittest.mock import MagicMock, patch

from rich.console import Console
from rich.table import Table
from rich.text import Text

from tests.support import load_exercise


class RichTerminalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_exercise("023_rich_terminal.py")

    def tasks(self):
        return [
            self.module.Task(1, "Write tests", "Ada", True),
            self.module.Task(2, "Ship release", "Grace", False),
        ]

    def test_status_is_styled_text(self) -> None:
        done = self.module.status_text(True)
        open_ = self.module.status_text(False)
        self.assertIsInstance(done, Text)
        self.assertEqual(done.plain, "✓ done")
        self.assertEqual(done.style, "green")
        self.assertEqual(open_.plain, "• open")
        self.assertEqual(open_.style, "yellow")

    def test_table_renders_headers_and_rows(self) -> None:
        table = self.module.build_task_table(self.tasks())
        self.assertIsInstance(table, Table)
        self.assertEqual([column.header for column in table.columns], ["ID", "Task", "Owner", "Status"])
        stream = StringIO()
        Console(file=stream, width=80, color_system=None).print(table)
        output = stream.getvalue()
        for text in ("Tasks", "Write tests", "Ship release", "Ada", "Grace", "✓ done", "• open"):
            self.assertIn(text, output)

    def test_dashboard_uses_supplied_console(self) -> None:
        stream = StringIO()
        console = Console(file=stream, width=80, color_system=None)
        self.module.render_dashboard(self.tasks(), console)
        self.assertIn("1/2 complete", stream.getvalue())

    def test_progress_calls_worker_and_advances(self) -> None:
        console = MagicMock(spec=Console)
        progress = MagicMock()
        progress.__enter__.return_value = progress
        progress.add_task.return_value = 42
        with patch.object(self.module, "Progress", return_value=progress) as Progress:
            result = self.module.process_with_progress([1, 2, 3], lambda value: value * 10, console)
        self.assertEqual(result, [10, 20, 30])
        self.assertIs(Progress.call_args.kwargs["console"], console)
        progress.add_task.assert_called_once_with("Processing", total=3)
        self.assertEqual(progress.advance.call_args_list, [unittest.mock.call(42)] * 3)
        progress.__exit__.assert_called_once()

    def test_progress_does_not_advance_failed_item(self) -> None:
        progress = MagicMock()
        progress.__enter__.return_value = progress
        progress.add_task.return_value = 7
        with patch.object(self.module, "Progress", return_value=progress):
            with self.assertRaisesRegex(ValueError, "bad"):
                self.module.process_with_progress([1], lambda _: (_ for _ in ()).throw(ValueError("bad")), MagicMock())
        progress.advance.assert_not_called()


if __name__ == "__main__":
    unittest.main()
