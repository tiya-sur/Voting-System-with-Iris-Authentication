import pandas as pd
from pathlib import Path
import hashlib

# Define database path
path = Path("database")

# Ensure database directory exists
path.mkdir(exist_ok=True)

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to reset voting counts
def count_reset():
    df = pd.read_csv(path / 'voterList.csv')
    df['hasVoted'] = 0  # Reset all voters to "has not voted"
    df.to_csv(path / 'voterList.csv', index=False)

    df = pd.read_csv(path / 'cand_list.csv')
    df['Vote Count'] = 0  # Reset vote counts for all candidates
    df.to_csv(path / 'cand_list.csv', index=False)

# Function to reset voter list
def reset_voter_list():
    df = pd.DataFrame(columns=['voter_id', 'Name', 'Gender', 'Zone', 'City', 'Passw', 'hasVoted'])
    df.to_csv(path / 'voterList.csv', index=False)

# Function to reset candidate list
def reset_cand_list():
    df = pd.DataFrame(columns=['Sign', 'Name', 'Vote Count'])
    df.to_csv(path / 'cand_list.csv', index=False)

# Function to verify voter credentials
def verify(vid, passw):
    df = pd.read_csv(path / 'voterList.csv')
    
    # Ensure 'Passw' column is treated as a string and strip whitespace
    df['Passw'] = df['Passw'].astype(str).str.strip()
    
    # Hash input password for comparison
    hashed_passw = hash_password(passw)
    
    # Debug: Print the hashed input password and the stored password
    print(f"Input Hashed Password: {hashed_passw}")
    print(f"Stored Passwords: {df['Passw'].tolist()}")
    
    # Check if the voter ID and password match
    for index, row in df.iterrows():
        if row['voter_id'] == vid and row['Passw'] == hashed_passw:
            print(f"Match found for Voter ID: {vid}")
            return True  # Password matches
    print(f"No match found for Voter ID: {vid}")
    return False  # Authentication failed

# Function to check if a voter is eligible to vote
def isEligible(vid):
    df = pd.read_csv(path / 'voterList.csv')
    voter = df[df['voter_id'] == vid]
    
    if not voter.empty and voter.iloc[0]['hasVoted'] == 0:
        return True
    return False

# Function to update vote count
def vote_update(st, vid):
    if isEligible(vid):
        df = pd.read_csv(path / 'cand_list.csv')

        # Update vote count
        df.loc[df['Sign'] == st, 'Vote Count'] += 1
        df.to_csv(path / 'cand_list.csv', index=False)

        # Mark voter as voted
        df = pd.read_csv(path / 'voterList.csv')
        df.loc[df['voter_id'] == vid, 'hasVoted'] = 1
        df.to_csv(path / 'voterList.csv', index=False)

        return True
    return False

# Function to display results
def show_result():
    df = pd.read_csv(path / 'cand_list.csv')
    results = df.set_index('Sign')['Vote Count'].to_dict()
    return results

# Function to add new voter data
def taking_data_voter(name, gender, zone, city, passw):
    try:
        df = pd.read_csv(path / 'voterList.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['voter_id', 'Name', 'Gender', 'Zone', 'City', 'Passw', 'hasVoted'])

    if df.empty:
        vid = 10001
    else:
        vid = df['voter_id'].max() + 1  # Get next voter ID

    # Hash password before storing
    hashed_passw = hash_password(passw)

    new_voter = pd.DataFrame({
        "voter_id": [vid],
        "Name": [name],
        "Gender": [gender],
        "Zone": [zone],
        "City": [city],
        "Passw": [hashed_passw],
        "hasVoted": [0]
    })

    df = pd.concat([df, new_voter], ignore_index=True)
    df.to_csv(path / 'voterList.csv', index=False)

    return vid