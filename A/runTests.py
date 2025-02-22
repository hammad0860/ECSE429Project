import os
import sys
import random
import pytest

if __name__ == "__main__":
    seed = random.randint(0, 10000)
    print(f"Using seed: {seed}")
    
    script_dir = os.path.dirname(os.path.realpath(__file__))
    test_dir = os.path.join(script_dir, "UnitTests")
    sys.exit(pytest.main([
        f"--randomly-seed={seed}",
        "-o", "python_files=*UnitTests.py",
        test_dir
    ]))
