"""Unit tests for validation functions."""

import pytest

from src.exceptions import (
    PaginationError,
    TaskValidationError,
    TerminalError,
    ValidationError,
)
from src.services.validators import (
    MAX_DESCRIPTION_CHARS,
    MAX_TITLE_WORDS,
    MIN_TERMINAL_WIDTH,
    TIMESTAMP_FORMAT,
    count_words,
    is_valid_id,
    is_valid_status,
    is_valid_timestamp,
    truncate_text,
    validate_description,
    validate_id,
    validate_non_empty_selection,
    validate_page_number,
    validate_status,
    validate_terminal_width,
    validate_timestamp,
    validate_title,
)


class TestValidateTitle:
    """Tests for validate_title function."""

    def test_valid_single_word_title(self) -> None:
        """Test that single word title is valid."""
        validate_title("Buy")
        # No exception raised

    def test_valid_multi_word_title(self) -> None:
        """Test that multi-word title is valid."""
        validate_title("Buy groceries today")
        # No exception raised

    def test_valid_title_with_max_words(self) -> None:
        """Test that title with exactly 10 words is valid."""
        validate_title("One two three four five six seven eight nine ten")
        # No exception raised

    def test_empty_title_raises_error(self) -> None:
        """Test that empty title raises TaskValidationError."""
        with pytest.raises(TaskValidationError, match="Title cannot be empty"):
            validate_title("")

    def test_whitespace_only_title_raises_error(self) -> None:
        """Test that whitespace-only title raises TaskValidationError."""
        with pytest.raises(TaskValidationError, match="Title cannot be empty"):
            validate_title("   ")

    def test_title_too_long_raises_error(self) -> None:
        """Test that title with more than 10 words raises TaskValidationError."""
        long_title = "One two three four five six seven eight nine ten eleven"
        with pytest.raises(TaskValidationError, match="Title too long"):
            validate_title(long_title)

    def test_title_strips_whitespace(self) -> None:
        """Test that leading/trailing whitespace is handled."""
        validate_title("  Buy groceries  ")
        # No exception raised


class TestValidateDescription:
    """Tests for validate_description function."""

    def test_empty_description_is_valid(self) -> None:
        """Test that empty description is valid (optional field)."""
        validate_description("")
        # No exception raised

    def test_short_description_is_valid(self) -> None:
        """Test that short description is valid."""
        validate_description("Milk, eggs, bread")
        # No exception raised

    def test_max_length_description_is_valid(self) -> None:
        """Test that description with exactly 500 characters is valid."""
        description = "a" * MAX_DESCRIPTION_CHARS
        validate_description(description)
        # No exception raised

    def test_description_too_long_raises_error(self) -> None:
        """Test that description with more than 500 characters raises error."""
        description = "a" * (MAX_DESCRIPTION_CHARS + 1)
        with pytest.raises(TaskValidationError, match="Description too long"):
            validate_description(description)

    def test_multiline_description_is_valid(self) -> None:
        """Test that multiline description is valid."""
        description = "Line 1\nLine 2\nLine 3"
        validate_description(description)
        # No exception raised


class TestValidateId:
    """Tests for validate_id function."""

    def test_valid_id_lowercase_hex(self) -> None:
        """Test that valid 8-char lowercase hex ID is accepted."""
        validate_id("abc123de")
        # No exception raised

    def test_valid_id_all_numbers(self) -> None:
        """Test that valid 8-char numeric ID is accepted."""
        validate_id("12345678")
        # No exception raised

    def test_valid_id_all_letters(self) -> None:
        """Test that valid 8-char letter-only hex ID is accepted."""
        validate_id("abcdefab")
        # No exception raised

    def test_uppercase_id_raises_error(self) -> None:
        """Test that uppercase hex characters raise error."""
        with pytest.raises(TaskValidationError, match="Invalid ID format"):
            validate_id("ABC123DE")

    def test_too_short_id_raises_error(self) -> None:
        """Test that ID shorter than 8 characters raises error."""
        with pytest.raises(TaskValidationError, match="Invalid ID format"):
            validate_id("abc123")

    def test_too_long_id_raises_error(self) -> None:
        """Test that ID longer than 8 characters raises error."""
        with pytest.raises(TaskValidationError, match="Invalid ID format"):
            validate_id("abc123def0")

    def test_invalid_characters_raises_error(self) -> None:
        """Test that non-hex characters raise error."""
        with pytest.raises(TaskValidationError, match="Invalid ID format"):
            validate_id("xyz12345")


class TestValidateStatus:
    """Tests for validate_status function."""

    def test_pending_status_is_valid(self) -> None:
        """Test that 'pending' status is valid."""
        validate_status("pending")
        # No exception raised

    def test_completed_status_is_valid(self) -> None:
        """Test that 'completed' status is valid."""
        validate_status("completed")
        # No exception raised

    def test_invalid_status_raises_error(self) -> None:
        """Test that invalid status raises error."""
        with pytest.raises(TaskValidationError, match="Invalid status"):
            validate_status("done")

    def test_case_sensitive_status(self) -> None:
        """Test that status is case-sensitive."""
        with pytest.raises(TaskValidationError, match="Invalid status"):
            validate_status("Pending")


class TestValidateTimestamp:
    """Tests for validate_timestamp function."""

    def test_valid_timestamp(self) -> None:
        """Test that valid timestamp format is accepted."""
        validate_timestamp("2025-12-18 10:30:45")
        # No exception raised

    def test_invalid_date_format_raises_error(self) -> None:
        """Test that invalid date format raises error."""
        with pytest.raises(TaskValidationError, match="Invalid timestamp format"):
            validate_timestamp("2025/12/18 10:30:45")

    def test_invalid_time_format_raises_error(self) -> None:
        """Test that invalid time format raises error."""
        with pytest.raises(TaskValidationError, match="Invalid timestamp format"):
            validate_timestamp("2025-12-18 10:30")

    def test_date_only_raises_error(self) -> None:
        """Test that date without time raises error."""
        with pytest.raises(TaskValidationError, match="Invalid timestamp format"):
            validate_timestamp("2025-12-18")

    def test_invalid_date_values_raises_error(self) -> None:
        """Test that invalid date values raise error."""
        with pytest.raises(TaskValidationError, match="Invalid timestamp format"):
            validate_timestamp("2025-13-40 10:30:45")


class TestValidateTerminalWidth:
    """Tests for validate_terminal_width function."""

    def test_minimum_width_is_valid(self) -> None:
        """Test that exactly 80 columns is valid."""
        validate_terminal_width(MIN_TERMINAL_WIDTH)
        # No exception raised

    def test_larger_width_is_valid(self) -> None:
        """Test that width larger than minimum is valid."""
        validate_terminal_width(120)
        # No exception raised

    def test_too_narrow_raises_error(self) -> None:
        """Test that width less than 80 raises error."""
        with pytest.raises(TerminalError, match="Terminal too narrow"):
            validate_terminal_width(79)


class TestValidatePageNumber:
    """Tests for validate_page_number function."""

    def test_first_page_is_valid(self) -> None:
        """Test that page 0 is valid."""
        validate_page_number(0, 5)
        # No exception raised

    def test_middle_page_is_valid(self) -> None:
        """Test that middle page is valid."""
        validate_page_number(2, 5)
        # No exception raised

    def test_last_page_is_valid(self) -> None:
        """Test that last valid page is accepted."""
        validate_page_number(4, 5)
        # No exception raised

    def test_negative_page_raises_error(self) -> None:
        """Test that negative page number raises error."""
        with pytest.raises(PaginationError, match="Invalid page number"):
            validate_page_number(-1, 5)

    def test_page_beyond_range_raises_error(self) -> None:
        """Test that page number >= max_page raises error."""
        with pytest.raises(PaginationError, match="Invalid page number"):
            validate_page_number(5, 5)


class TestValidateNonEmptySelection:
    """Tests for validate_non_empty_selection function."""

    def test_single_item_selection_is_valid(self) -> None:
        """Test that single item selection is valid."""
        validate_non_empty_selection(["abc123de"])
        # No exception raised

    def test_multiple_item_selection_is_valid(self) -> None:
        """Test that multiple item selection is valid."""
        validate_non_empty_selection(["abc123de", "def456gh"])
        # No exception raised

    def test_empty_selection_raises_error(self) -> None:
        """Test that empty selection raises error."""
        with pytest.raises(ValidationError, match="No tasks selected"):
            validate_non_empty_selection([])


class TestIsValidId:
    """Tests for is_valid_id helper function."""

    def test_valid_id_returns_true(self) -> None:
        """Test that valid ID returns True."""
        assert is_valid_id("abc123de") is True

    def test_invalid_id_returns_false(self) -> None:
        """Test that invalid ID returns False."""
        assert is_valid_id("invalid") is False


class TestIsValidStatus:
    """Tests for is_valid_status helper function."""

    def test_pending_returns_true(self) -> None:
        """Test that 'pending' returns True."""
        assert is_valid_status("pending") is True

    def test_completed_returns_true(self) -> None:
        """Test that 'completed' returns True."""
        assert is_valid_status("completed") is True

    def test_invalid_status_returns_false(self) -> None:
        """Test that invalid status returns False."""
        assert is_valid_status("done") is False


class TestIsValidTimestamp:
    """Tests for is_valid_timestamp helper function."""

    def test_valid_timestamp_returns_true(self) -> None:
        """Test that valid timestamp returns True."""
        assert is_valid_timestamp("2025-12-18 10:30:45") is True

    def test_invalid_timestamp_returns_false(self) -> None:
        """Test that invalid timestamp returns False."""
        assert is_valid_timestamp("invalid") is False


class TestCountWords:
    """Tests for count_words helper function."""

    def test_single_word(self) -> None:
        """Test counting single word."""
        assert count_words("Buy") == 1

    def test_multiple_words(self) -> None:
        """Test counting multiple words."""
        assert count_words("Buy groceries today") == 3

    def test_extra_spaces(self) -> None:
        """Test that extra spaces are handled correctly."""
        assert count_words("  Buy   groceries  ") == 2

    def test_empty_string(self) -> None:
        """Test counting words in empty string."""
        assert count_words("") == 0


class TestTruncateText:
    """Tests for truncate_text helper function."""

    def test_short_text_not_truncated(self) -> None:
        """Test that short text is not truncated."""
        assert truncate_text("Short", 10) == "Short"

    def test_exact_length_text_not_truncated(self) -> None:
        """Test that text at exact max length is not truncated."""
        assert truncate_text("Exactly10!", 10) == "Exactly10!"

    def test_long_text_truncated(self) -> None:
        """Test that long text is truncated with suffix."""
        result = truncate_text("Very long text here", 10)
        assert result == "Very lo..."
        assert len(result) == 10

    def test_custom_suffix(self) -> None:
        """Test truncation with custom suffix."""
        result = truncate_text("Long text", 8, suffix=">>")
        assert result == "Long t>>"
        assert len(result) == 8
