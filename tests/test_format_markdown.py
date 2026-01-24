import json
import pytest
from io import StringIO
from unittest.mock import patch
from modules.job_search.components.format_markdown import format_salary, main


def test_format_salary():
    """Test salary formatting with various combinations of min/max."""
    # Both min and max
    assert (
        format_salary({"salary_min": 30000, "salary_max": 40000}) == "£30,000 - £40,000"
    )

    # Only min
    assert format_salary({"salary_min": 35000, "salary_max": None}) == "£35,000+"

    # Only max
    assert format_salary({"salary_min": None, "salary_max": 50000}) == "Up to £50,000"

    # Neither
    assert (
        format_salary({"salary_min": None, "salary_max": None})
        == "Salary not specified"
    )
    assert format_salary({}) == "Salary not specified"


def test_main_output():
    """Test the main function with sample JSON input."""
    sample_data = [
        {
            "title": "Software Engineer",
            "company": "Tech Corp",
            "location": "Remote",
            "salary_min": 50000,
            "salary_max": 70000,
            "description": "A great role for python devs.",
            "redirect_url": "http://example.com/apply",
            "agent_notes": "Highly recommended.",
        }
    ]

    input_json = json.dumps(sample_data)

    with patch("sys.stdin", StringIO(input_json)):
        with patch("sys.stdout", new=StringIO()) as mock_stdout:
            main()
            output = mock_stdout.getvalue()

            assert "# Job Search Results" in output
            assert "Software Engineer" in output
            assert "Tech Corp" in output
            assert "£50,000 - £70,000" in output
            assert "http://example.com/apply" in output
            assert "Highly recommended." in output


def test_main_invalid_json():
    """Test main function with invalid JSON input."""
    with patch("sys.stdin", StringIO("invalid json")):
        with patch("sys.stderr", new=StringIO()) as mock_stderr:
            with pytest.raises(SystemExit) as excinfo:
                main()
            assert excinfo.value.code == 1
            assert "Error: Invalid JSON input" in mock_stderr.getvalue()
