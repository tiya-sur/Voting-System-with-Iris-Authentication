# test_import.py
try:
    from VotingPage import votingPg
    print("Import successful!")
except ModuleNotFoundError as e:
    print(f"Import error: {e}")
