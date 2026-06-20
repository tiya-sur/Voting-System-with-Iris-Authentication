
    
    # iris_matching.py
import numpy as np
import database_module

def match_iris_template(features):
    try:
        database_features = database_module.get_all_iris_features()
        if database_features is None:
            print("Error: Database retrieval failed.") #debugging.
            return False, "Database error."
        print("Database Features Retrieved.") #debugging.
        for stored_features in database_features:
            print("Comparing:", features, "with:", stored_features) #debugging.
            if np.array_equal(features, stored_features):
                print("Match found.") #debugging.
                return True, "Iris match found."
        print("No match found.") #debugging.
        return False, "Iris match not found."
    except Exception as e:
        print(f"Matching error: {e}") #debugging.
        return False, "Matching error."