from src.sanber_training import version
import pytest

def test_version():
    assert version == "0.1.0"
    
if __name__ == "__main__":
    pytest.main()