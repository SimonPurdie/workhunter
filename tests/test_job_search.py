import pytest
from unittest.mock import patch, MagicMock
from modules.job_search.components.adzuna import AdzunaClient, RateLimitExceeded
from shared_formats.types import SearchCriteria


@pytest.fixture
def mock_adzuna_response():
    return {
        "results": [
            {
                "id": "123",
                "title": "Python Developer",
                "company": {"display_name": "Test Co"},
                "location": {"display_name": "London"},
                "salary_min": 50000,
                "salary_max": 60000,
                "description": "A test job",
                "redirect_url": "http://example.com",
                "created": "2026-01-01T00:00:00Z",
                "category": {"label": "IT Jobs"},
                "contract_time": "full_time",
                "contract_type": "permanent",
            }
        ]
    }


def test_adzuna_client_search(mock_adzuna_response):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_adzuna_response

        # We need to mock UsageTracker to avoid state file issues during tests
        with patch("modules.job_search.components.adzuna.UsageTracker") as mock_tracker:
            mock_tracker.return_value.check_and_increment.return_value = True

            client = AdzunaClient()
            criteria = SearchCriteria(keywords="Python", location="London")
            results = client.search_jobs(criteria)

            assert len(results) == 1
            assert results[0].id == "123"
            assert results[0].title == "Python Developer"


def test_adzuna_client_rate_limit():
    with patch("modules.job_search.components.adzuna.UsageTracker") as mock_tracker:
        mock_tracker.return_value.check_and_increment.return_value = False
        mock_tracker.return_value.get_limit_info.return_value = {
            "current": {"minute": 25},
            "limits": {"minute": 25},
        }

        client = AdzunaClient()
        criteria = SearchCriteria(keywords="Python", location="London")

        with pytest.raises(RateLimitExceeded) as exc_info:
            client.search_jobs(criteria)

        assert "rate limit exceeded" in str(exc_info.value)
        assert exc_info.value.limit_info["current"]["minute"] == 25
