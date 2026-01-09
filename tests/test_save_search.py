import pytest
import json
import subprocess
from pathlib import Path
from datetime import datetime


@pytest.fixture
def example_json_path():
    """Path to the example agent output JSON file."""
    script_dir = Path(__file__).parent.parent
    return script_dir / "scripts" / "job_search" / "example_agent_output.json"


@pytest.fixture
def save_search_script_path():
    """Path to the save_search.py script."""
    script_dir = Path(__file__).parent.parent
    return script_dir / "scripts" / "job_search" / "save_search.py"


@pytest.fixture
def workspace_dir():
    """Path to the workspace directory."""
    script_dir = Path(__file__).parent.parent
    return script_dir / "workspace"


def test_save_search_creates_files_and_outputs_json(example_json_path, save_search_script_path, workspace_dir):
    """Test that save_search.py creates JSON and markdown files and outputs success JSON."""
    # Read the example JSON input
    with open(example_json_path, 'r') as f:
        input_json = json.load(f)
    
    input_json_str = json.dumps(input_json)
    
    # Run save_search.py with the JSON input
    result = subprocess.run(
        ['uv', 'run', str(save_search_script_path)],
        input=input_json_str,
        capture_output=True,
        text=True,
        cwd=workspace_dir.parent  # Run from project root
    )
    
    # Verify the script ran successfully
    assert result.returncode == 0, f"Script failed with stderr: {result.stderr}"
    
    # Parse the output JSON
    output_data = json.loads(result.stdout)
    
    # Verify output structure
    assert output_data['status'] == 'success'
    assert 'files_created' in output_data
    assert 'job_count' in output_data
    assert output_data['job_count'] == len(input_json)
    
    # Verify files were created
    files_created = output_data['files_created']
    assert len(files_created) == 2  # JSON and markdown files
    
    json_file_path = Path(files_created[0])
    md_file_path = Path(files_created[1])
    
    # Verify files exist
    assert json_file_path.exists(), f"JSON file {json_file_path} was not created"
    assert md_file_path.exists(), f"Markdown file {md_file_path} was not created"
    
    # Verify JSON file content matches input
    with open(json_file_path, 'r') as f:
        saved_json = json.load(f)
    
    assert saved_json == input_json, "Saved JSON content doesn't match input"
    
    # Verify markdown file content structure
    with open(md_file_path, 'r') as f:
        md_content = f.read()
    
    # Check for expected markdown structure
    assert "# Job Search Results" in md_content
    assert f"**Total Results**: {len(input_json)}" in md_content
    
    # Check that all job titles appear in the markdown
    for job in input_json:
        assert job['title'] in md_content
        assert job['company'] in md_content
        assert job['location'] in md_content
        # Check for agent notes if present
        if job.get('agent_notes'):
            assert job['agent_notes'] in md_content
    
    # Cleanup: Remove the created files
    json_file_path.unlink(missing_ok=True)
    md_file_path.unlink(missing_ok=True)
    
    # Cleanup: Remove workspace directory if it's empty
    if workspace_dir.exists() and not any(workspace_dir.iterdir()):
        workspace_dir.rmdir()


def test_save_search_file_naming(example_json_path, save_search_script_path, workspace_dir):
    """Test that files are named correctly with date pattern."""
    # Read the example JSON input
    with open(example_json_path, 'r') as f:
        input_json = json.load(f)
    
    input_json_str = json.dumps(input_json)
    
    # Run save_search.py
    result = subprocess.run(
        ['uv', 'run', str(save_search_script_path)],
        input=input_json_str,
        capture_output=True,
        text=True,
        cwd=workspace_dir.parent
    )
    
    assert result.returncode == 0
    
    output_data = json.loads(result.stdout)
    files_created = output_data['files_created']
    
    # Verify file naming pattern: jobsearch_YYYYMMDD_N.{json,md}
    date_str = datetime.now().strftime("%Y%m%d")
    expected_pattern = f"jobsearch_{date_str}_"
    
    for file_path_str in files_created:
        file_path = Path(file_path_str)
        file_name = file_path.name
        assert file_name.startswith(expected_pattern), f"File {file_name} doesn't match expected pattern"
        assert file_name.endswith(('.json', '.md')), f"File {file_name} doesn't have .json or .md extension"
    
    # Cleanup
    for file_path_str in files_created:
        Path(file_path_str).unlink(missing_ok=True)
    
