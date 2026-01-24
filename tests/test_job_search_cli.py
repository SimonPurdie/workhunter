import json
import pytest
import sys
from io import StringIO
from unittest.mock import patch, MagicMock
from modules.job_search.job_search import main
from shared_formats.types import JobListing


@pytest.fixture
def mock_job():
    return JobListing(
        id="123",
        title="Python Developer",
        company="Test Co",
        location="London",
        salary_min=50000,
        salary_max=60000,
        description="A test job",
        redirect_url="http://example.com",
        created="2026-01-01T00:00:00Z",
    )


def test_job_search_main_success(mock_job):
    """Test successful run of the CLI main function."""
    with patch("modules.job_search.job_search.AdzunaClient") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_client.search_jobs.return_value = [mock_job]

        with patch(
            "modules.job_search.job_search.job_tracker.load_seen_jobs", return_value=[]
        ):
            with patch("sys.stdout", new=StringIO()) as mock_stdout:
                # Set CLI arguments
                test_args = [
                    "job_search.py",
                    "--keywords",
                    "Python",
                    "--location",
                    "London",
                    "--target-count",
                    "1",
                ]
                with patch("sys.argv", test_args):
                    main()

                    output = json.loads(mock_stdout.getvalue())
                    assert len(output) == 1
                    assert output[0]["title"] == "Python Developer"


def test_job_search_pagination(mock_job):
    """Test that pagination loop works until target-count is reached."""
    with patch("modules.job_search.job_search.AdzunaClient") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        # Return 1 job per call
        mock_client.search_jobs.side_effect = [[mock_job], [mock_job], []]

        with patch(
            "modules.job_search.job_search.job_tracker.load_seen_jobs", return_value=[]
        ):
            with patch("sys.stdout", new=StringIO()) as mock_stdout:
                test_args = [
                    "job_search.py",
                    "--keywords",
                    "Python",
                    "--location",
                    "London",
                    "--target-count",
                    "2",
                    "--results-per-page",
                    "1",
                ]
                with patch("sys.argv", test_args):
                    main()

                    # Should have called search_jobs twice to get 2 jobs
                    assert mock_client.search_jobs.call_count >= 2
                    output = json.loads(mock_stdout.getvalue())
                    # Since it's the same job, it might get deduplicated if we aren't careful
                    # But wait, job_search.py deduplicates against SEEN hashes from tracker.
                    # Within the same run, it doesn't explicitly deduplicate against 'all_matches'
                    # unless they are already in seen_hashes.
                    # In my mock, I return the same mock_job twice.
                    assert len(output) == 2


def test_job_search_deduplication(mock_job):
    """Test that already seen jobs are filtered out."""
    with patch("modules.job_search.job_search.AdzunaClient") as mock_client_cls:
        mock_client = mock_client_cls.return_value
        mock_client.search_jobs.return_value = [mock_job]

        # Mock tracker to return the hash of our mock_job as seen
        from modules.job_search.components.job_tracker import generate_hash

        job_hash = generate_hash(mock_job.company, mock_job.title, mock_job.location)

        with patch(
            "modules.job_search.job_search.job_tracker.load_seen_jobs",
            return_value=[{"hash": job_hash}],
        ):
            with patch("sys.stdout", new=StringIO()) as mock_stdout:
                test_args = [
                    "job_search.py",
                    "--keywords",
                    "Python",
                    "--location",
                    "London",
                ]
                with patch("sys.argv", test_args):
                    main()

                    output = json.loads(mock_stdout.getvalue())
                    assert len(output) == 0
