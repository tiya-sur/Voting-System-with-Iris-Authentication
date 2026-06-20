# database_module.py
# database_module.py
import numpy as np
import sqlite3

DATABASE_FILE = "iris_database.db"

def create_connection():
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS iris_features (
                    label TEXT PRIMARY KEY,
                    features BLOB
                )
            """)
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()

def store_iris_features(features, label):
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            features_blob = features.tobytes()
            cursor.execute("INSERT OR REPLACE INTO iris_features (label, features) VALUES (?, ?)", (label, features_blob))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error storing iris features: {e}")
            return False
        finally:
            conn.close()
    return False

def get_all_iris_features():
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT label, features FROM iris_features")
            rows = cursor.fetchall()
            features_dict = {}
            for row in rows:
                label = row[0]
                features_blob = row[1]
                features = np.frombuffer(features_blob, dtype=np.float32) # adjust the dtype as needed.
                features_dict[label] = features
            return features_dict
        except sqlite3.Error as e:
            print(f"Error retrieving iris features: {e}")
            return None
        finally:
            conn.close()
    return None

create_table()

def get_all_iris_features():
    try:
        
        example_database = [np.array([1,2,3,4,5]), np.array([6,7,8,9,10])] #example database.
        print("Database retrieval successful.") #debugging.
        return example_database
    except Exception as e:
        print(f"Database error: {e}") #debugging.
        return None
    


def store_iris_features(features):
    print("Iris features stored.")
    return True

def get_all_iris_features():
    try:
       
        example_database = [np.array([1, 2, 3, 4, 5]), np.array([6, 7, 8, 9, 10])]
        print("Database retrieval successful.")  # Debugging
        return example_database
    except Exception as e:
        print(f"Database error: {e}")  # Debugging
        return None

def match_iris_template(features):
    try:
        database_features = get_all_iris_features()  
        if database_features is None:
            print("Error: Database retrieval failed.")  # Debugging
            return False, "Database error."
        for stored_features in database_features:
            if np.array_equal(features, stored_features):
                print("Match found.")  # Debugging
                return True, "Iris match found."
        print("No match found.")  # Debugging
        return False, "Iris match not found."
    except Exception as e:
        print(f"Matching error: {e}")  # Debugging
        return False, "Matching error."