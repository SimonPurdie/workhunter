import pytest
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from datetime import datetime

from modules.job_applications.claim_job import (
    slugify_company,
    get_next_application_folder,
    claim_job,
)


class TestSlugifyCompany:
    """Test the slugify_company function"""

    def test_basic_slugify(self):
        assert slugify_company("Technological Solutions Inc.") == "technological-so"

    def test_special_characters(self):
        assert slugify_company("Tech & Co.!") == "tech-co"

    def test_long_company_name(self):
        long_name = "A" * 50
        result = slugify_company(long_name)
        assert len(result) <= 16
        assert result == "a" * 16

    def test_empty_company(self):
        assert slugify_company("") == ""

    def test_numbers_and_letters(self):
        assert slugify_company("123 Tech Company 456") == "123-tech-company"


class TestGetNextApplicationFolder:
    """Test the get_next_application_folder function"""

    @pytest.fixture
    def temp_apps_dir(self):
        """Create a temporary directory for testing"""
        temp_dir = Path(tempfile.mkdtemp())
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_new_folder_no_existing(self, temp_apps_dir):
        """Test creating first folder of the day"""
        job_record = {"company": "Test Company"}

        with patch("modules.job_applications.claim_job.APPS_DIR", temp_apps_dir):
            result = get_next_application_folder(job_record)

            date_str = datetime.now().strftime("%Y%m%d")
            expected_name = f"{date_str}-1-test-company"
            assert result.name == expected_name

    def test_increment_counter_existing_folders(self, temp_apps_dir):
        """Test counter increment with existing folders"""
        date_str = datetime.now().strftime("%Y%m%d")

        # Create existing folders
        (temp_apps_dir / f"{date_str}-1-company-a").mkdir()
        (temp_apps_dir / f"{date_str}-2-company-b").mkdir()

        job_record = {"company": "New Company"}

        with patch("modules.job_applications.claim_job.APPS_DIR", temp_apps_dir):
            result = get_next_application_folder(job_record)

            expected_name = f"{date_str}-3-new-company"
            assert result.name == expected_name

    def test_unknown_company_fallback(self, temp_apps_dir):
        """Test fallback to 'unknown' when company is missing"""
        job_record = {}  # No company field

        with patch("modules.job_applications.claim_job.APPS_DIR", temp_apps_dir):
            result = get_next_application_folder(job_record)

            date_str = datetime.now().strftime("%Y%m%d")
            expected_name = f"{date_str}-1-unknown"
            assert result.name == expected_name

    def test_ignore_different_date_folders(self, temp_apps_dir):
        """Test that only current date folders are counted"""
        date_str = datetime.now().strftime("%Y%m%d")
        old_date = "20250101"

        # Create old date folder that should be ignored
        (temp_apps_dir / f"{old_date}-5-old-company").mkdir()

        job_record = {"company": "Today Company"}

        with patch("modules.job_applications.claim_job.APPS_DIR", temp_apps_dir):
            result = get_next_application_folder(job_record)

            # Should start from 1, not 6
            expected_name = f"{date_str}-1-today-company"
            assert result.name == expected_name


class TestClaimJobIntegration:
    """Integration test for the full claim_job process"""

    @pytest.fixture
    def temp_work(self):
        """Create temporary work directories"""
        temp_dir = Path(tempfile.mkdtemp())
        work = temp_dir / "work" / "roles"
        queue_dir = work / "queue"
        apps_dir = work
        queue_dir.mkdir(parents=True)

        yield {"work_dir": work, "queue_dir": queue_dir, "apps_dir": apps_dir}

        shutil.rmtree(temp_dir)

    def test_claim_single_job(self, temp_work):
        """Test claiming a single job from queue"""
        # Create test job in queue
        test_job = {
            "title": "Python Developer",
            "company": "Technological Solutions Inc.",
            "location": "Remote",
            "salary": "100000",
        }

        queue_file = temp_work["queue_dir"] / "jobs.json"
        with open(queue_file, "w") as f:
            json.dump([test_job], f)

        # Mock the paths
        with patch(
            "modules.job_applications.claim_job.QUEUE_DIR", temp_work["queue_dir"]
        ):
            with patch(
                "modules.job_applications.claim_job.APPS_DIR",
                temp_work["apps_dir"],
            ):
                claim_job()

        # Verify job was moved
        date_str = datetime.now().strftime("%Y%m%d")
        expected_dir = temp_work["apps_dir"] / f"{date_str}-1-technological-so"

        assert expected_dir.exists()
        assert (expected_dir / "job.json").exists()

        # Verify queue file was removed (empty)
        assert not queue_file.exists()

        # Verify job content
        with open(expected_dir / "job.json") as f:
            moved_job = json.load(f)
            assert moved_job["company"] == "Technological Solutions Inc."

    def test_claim_multiple_jobs_keeps_remaining(self, temp_work):
        """Test claiming one job when multiple are in queue"""
        # Create test jobs in queue
        job1 = {"title": "Python Developer", "company": "Company A"}
        job2 = {"title": "React Developer", "company": "Company B"}

        queue_file = temp_work["queue_dir"] / "jobs.json"
        with open(queue_file, "w") as f:
            json.dump([job1, job2], f)

        # Claim first job
        with patch(
            "modules.job_applications.claim_job.QUEUE_DIR", temp_work["queue_dir"]
        ):
            with patch(
                "modules.job_applications.claim_job.APPS_DIR",
                temp_work["apps_dir"],
            ):
                claim_job()

        # Verify first job was moved
        date_str = datetime.now().strftime("%Y%m%d")
        first_dir = temp_work["apps_dir"] / f"{date_str}-1-company-a"
        assert first_dir.exists()

        # Verify second job remains in queue
        assert queue_file.exists()
        with open(queue_file) as f:
            remaining_jobs = json.load(f)
            assert len(remaining_jobs) == 1
            assert remaining_jobs[0]["company"] == "Company B"

    def test_empty_queue_no_error(self, temp_work):
        """Test handling of empty queue"""
        with patch(
            "modules.job_applications.claim_job.QUEUE_DIR", temp_work["queue_dir"]
        ):
            with patch(
                "modules.job_applications.claim_job.APPS_DIR",
                temp_work["apps_dir"],
            ):
                # Should not raise an exception
                claim_job()

        # No directories should be created (except the queue dir which exists by setup)
        apps_contents = [
            p for p in temp_work["apps_dir"].iterdir() if p.name != "queue"
        ]
        queue_contents = list(temp_work["queue_dir"].iterdir())
        assert len(apps_contents) == 0
        assert len(queue_contents) == 0
