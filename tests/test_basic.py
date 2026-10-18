def test_basic_python_check():
    assert 1 + 1 == 2


def test_project_folder_exists():
    from pathlib import Path
    assert Path("data").exists()
