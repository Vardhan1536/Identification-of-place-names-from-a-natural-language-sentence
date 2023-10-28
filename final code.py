import sqlite3
from fuzzywuzzy import fuzz

# Create a function to identify and map place names from a sentence
def find_and_map_place_names(sentence, table_name, cursor):
    canonical_names = []

    # Tokenize the sentence by splitting it into words
    tokens = sentence.split()

    # Iterate through the tokens in the sentence
    for token in tokens:
        # Check if the token is a place name (e.g., country, city, state)
        if token.lower() not in ['of', 'the', 'in', 'for', 'a', 'an']:
            cursor.execute(f"SELECT name FROM {table_name}")
            rows = cursor.fetchall()

            # Create a set to store unique exact matches
            exact_matches = set()

            for row in rows:
                name = row[0]
                # Check for an exact match
                if token.lower() == name.lower():
                    exact_matches.add(name)

            # If there are exact matches, prioritize them
            if exact_matches:
                for name in exact_matches:
                    canonical_names.append({
                        "token": token,
                        "canonical_name": name,
                        "table": table_name
                    })
            # If there are no exact matches, use fuzzy matching
            else:
                for row in rows:
                    name = row[0]
                    similarity = fuzz.ratio(token.lower(), name.lower())
                    if similarity > 80:  # Adjust the similarity threshold as needed
                        canonical_names.append({
                            "token": token,
                            "canonical_name": name,
                            "table": table_name
                        })

    return canonical_names

# Connect to the SQLite database
conn = sqlite3.connect('geospatialdata.db')
cursor = conn.cursor()

# Take user input for a sentence
input_sentence = input("Enter a sentence: ")

# Identify place names and map them to canonical names from the database
place_names = []
place_names.extend(find_and_map_place_names(input_sentence, 'Countries', cursor))
place_names.extend(find_and_map_place_names(input_sentence, 'States', cursor))
place_names.extend(find_and_map_place_names(input_sentence, 'Cities', cursor))

# Print the results
for place in place_names:
    print(f"Token: {place['token']}, Canonical Name: {place['canonical_name']}, Table: {place['table']}")

# Close the database connection
conn.close()
