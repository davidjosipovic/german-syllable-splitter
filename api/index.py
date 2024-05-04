from flask import Flask
from spylls.hunspell import Dictionary
from split_words import Splitter
app = Flask(__name__)
splitter = Splitter()

 
def is_german_word(word):
    dictionary = Dictionary.from_files('dictionary/de_DE')
    return dictionary.lookup(word)



def split_and_check_german(word, level=0):
    indent = "    " * level
    compounds = []

    # Split the compound word into parts
    splits = splitter.split_compound(word)

    print(f"{indent}Splitting: {word}")

    # If there are no splits, return an empty list
    if not splits:
        print(f"{indent}No splits found for {word}")
        return []

    # Get the first and second parts of the split
    for i in range(min(len(splits), 3)):
        first_part = splits[i][1]
        second_part = splits[i][2]

        print(f"{indent}Checking parts: {first_part}, {second_part}")

        if first_part == second_part:
            print(f"{indent}Equal parts found: {first_part}")
            return [first_part]
        

        # Check if the first or second parts are German words
        if is_german_word(first_part) and is_german_word(second_part):
            print(f"{indent}German word found: {first_part} and {second_part}")

            # Recursively split and check each part if they are German
            first_split = split_and_check_german(first_part, level + 1)
            second_split = split_and_check_german(second_part, level + 1)

            # Combine splits if both parts are German
            if first_split and second_split:
                compounds.extend(first_split)
                compounds.extend(second_split)
            else:
                compounds.append(first_part)
                compounds.append(second_part)
            break  # Break the loop if German word found
        else:
            print(f"{indent}Not German words: {first_part} and {second_part}")
    
    if compounds==[]:
        compounds=[word]
    
    return compounds


# Define the compound word
compound_word = 'Autobahnanschlussstelle'

# Call the function to split and check if the parts are German
final_split = split_and_check_german(compound_word)

# Join the compounds into a single string with spaces
final_string = ' '.join(final_split)





@app.route("/api/python")
def hello_world():
    return final_string