import pytest
from scripts.job_search.lib.engine import Engine
from shared.types import JobListing, SearchCriteria

@pytest.fixture
def sample_criteria():
    return SearchCriteria(
        keywords="Python Developer",
        location="London",
        salary_min=50000
    )

@pytest.fixture
def sample_jobs():
    return [
        JobListing(
            id="1",
            title="Senior Python Developer",
            company="Tech Corp",
            location="London",
            salary_min=60000,
            description="Leading python role...",
            redirect_url="http://example.com/1",
            created="2026-01-01T00:00:00Z"
        ),
        JobListing(
            id="2",
            title="Junior Data Analyst",
            company="Data Inc",
            location="London",
            salary_min=30000,
            description="Junior analyst role...",
            redirect_url="http://example.com/2",
            created="2026-01-01T00:00:00Z"
        ),
        JobListing(
            id="3",
            title="Python Software Engineer",
            company="Web Soft",
            location="Manchester",
            salary_min=55000,
            description="Python engineering...",
            redirect_url="http://example.com/3",
            created="2026-01-01T00:00:00Z"
        )
    ]

def test_engine_filter_jobs(sample_criteria, sample_jobs):
    engine = Engine(sample_criteria)
    filtered = engine.filter_jobs(sample_jobs)
    
    # "Python Developer" matches "Senior Python Developer" and "Python Software Engineer"
    # because of keyword matching logic (any kw in title)
    assert len(filtered) == 2
    titles = [j.title for j in filtered]
    assert "Senior Python Developer" in titles
    assert "Python Software Engineer" in titles
    assert "Junior Data Analyst" not in titles

def test_engine_rank_jobs(sample_criteria, sample_jobs):
    engine = Engine(sample_criteria)
    # Filter first to get the 2 relevant jobs
    filtered = engine.filter_jobs(sample_jobs)
    ranked = engine.rank_jobs(filtered)
    
    assert len(ranked) == 2
    # Senior Python Developer should be first due to more keywords/salary
    assert ranked[0].title == "Senior Python Developer"
