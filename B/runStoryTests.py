import random
import pytest
import os
import subprocess
import glob

@pytest.mark.order
def test_features(request):
    RANDOM_SEED = request.config.getoption("--randomly-seed", default=random.randint(1, 999999))
    random.seed(RANDOM_SEED)
    print(f"Using seed: {RANDOM_SEED}")

    features_dir = os.path.join(os.getcwd(), "features")
    
    feature_files = glob.glob(os.path.join(features_dir, "**/*.feature"), recursive=True)
    
    feature_files = [os.path.relpath(f, features_dir) for f in feature_files]
    
    random.shuffle(feature_files)
    print("Shuffled feature file order:")
    for f in feature_files:
        print(f)
    

    cmd = "behave " + " ".join(feature_files)
    
    process = subprocess.Popen(cmd, cwd=features_dir, shell=True)
    process.wait()
    exit_code = process.returncode

    assert exit_code == 0, "Behave tests failed"
