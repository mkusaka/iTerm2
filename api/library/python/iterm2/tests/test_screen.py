"""Tests for iterm2.screen module."""
import iterm2.api_pb2 as api_pb2
from iterm2.screen import LineContents


class TestLineContents:
    """Tests for the LineContents class."""

    @staticmethod
    def make_line(text, code_points_per_cell):
        """Build a LineContents proto for tests."""
        line = api_pb2.LineContents(text=text)
        for num_code_points, repeats in code_points_per_cell:
            cpp = line.code_points_per_cell.add()
            cpp.num_code_points = num_code_points
            cpp.repeats = repeats
        return LineContents(line)

    def test_string_renders_uninitialized_cells_as_spaces(self):
        """Mid-line uninitialized cells should render as blank columns."""
        line = self.make_line("abcxyz", [(1, 3), (0, 3), (1, 3)])

        assert line.string == "abc   xyz"
        assert line.string_at(2) == "c"
        assert line.string_at(3) == ""
        assert line.string_at(6) == "x"

    def test_string_preserves_multicodepoint_cells(self):
        """Multi-code-point cells should survive display reconstruction."""
        line = self.make_line("an\u0303b", [(1, 1), (0, 1), (2, 1), (1, 1)])

        assert line.string == "a n\u0303b"
        assert line.string_at(0) == "a"
        assert line.string_at(1) == ""
        assert line.string_at(2) == "n\u0303"
        assert line.string_at(3) == "b"

    def test_string_falls_back_to_raw_text_without_cell_map(self):
        """Older responses without cell metadata should keep raw text."""
        line = self.make_line("abc\x00xyz", [])

        assert line.string == "abc\x00xyz"
