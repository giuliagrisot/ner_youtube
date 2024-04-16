#   NAMED ENTITY RECOGNITION SERIES   #
#             Lesson 04               #
#        Leveraging spaCy's NER       #
#               with                  #
#        Dr. W.J.B. Mattingly         #
import spacy
from spacy.lang.en import English
from spacy.pipeline import EntityRuler
import json

#  In this lesson we will be leveraging spaCy's NER to create a custom NER model
#  We will be using the Harry Potter series as our training data
#  We will be using the Harry Potter series as our test data

#  The first thing we need to do is load the data from the JSON file. We can define a function to do this for us, which we can include in our code later
def load_data(file): # This function will load the data from a JSON file
    with open(file, "r", encoding="utf-8") as f: # We are opening the file in read mode
        data = json.load(f) # We are loading the data from the file
    return (data)   # We are returning the data

#  Next we need to save the data to a JSON file. Again, we are creatig a function to do this for us
def save_data(file, data): # This function will save the data to a JSON file
    with open (file, "w", encoding="utf-8") as f: # We are opening the file in write mode
        json.dump(data, f, indent=4) # We are writing the data to the file

#  Now we need to generate a list of characters from the Harry Potter series. We can define a function to do this for us. How does this function work? It loads the data from the JSON file, generates a list of characters, removes certain words from the list, splits the items in the list, removes any leading or trailing whitespace from the names, removes any duplicates from the list, sorts the list, and returns the list.
def generate_better_characters(file): # This function will generate a list of characters from the Harry Potter series
    data = load_data(file) # We are loading the data from the file
    print (len(data))  # We are printing the number of items in the data
    new_characters = [] # We are creating an empty list to store the characters
    for item in data: # We are iterating over the items in the data
        new_characters.append(item) # We are adding the item to the list
    for item in data: # We are iterating over the items in the data
        item = item.replace("The", "").replace("the", "").replace("and", "").replace("And", "") # We are removing certain words from the item
        names = item.split(" ") # We are splitting the item into a list of names
        for name in names: # We are iterating over the names in the list
            name = name.strip() # We are removing any leading or trailing whitespace from the name
            new_characters.append(name) # We are adding the name to the list
        if "(" in item: # We are checking if the item contains a "("
            names = item.split("(") # We are splitting the item at the "("
            for name in names:  # We are iterating over the names in the list
                name = name.replace(")", "").strip() # We are removing the ")" and any leading or trailing whitespace from the name
                new_characters.append(name) # We are adding the name to the list
        if "," in item: # We are checking if the item contains a ","
            names = item.split(",") # We are splitting the item at the ","
            for name in names: # We are iterating over the names in the list
                name = name.replace("and", "").strip() # We are removing "and" and any leading or trailing whitespace from the name
                if " " in name: # We are checking if the name contains a " "
                    new_names = name.split() # We are splitting the name into a list of new names
                    for x in new_names: # We are iterating over the new names in the list
                        x = x.strip() # We are removing any leading or trailing whitespace from the new name
                        new_characters.append(x) # We are adding the new name to the list
                new_characters.append(name) # We are adding the name to the list
    print (len(new_characters)) # We are printing the number of items in the list
    final_characters = [] # We are creating an empty list to store the final characters
    titles = ["Dr.", "Professor", "Mr.", "Mrs.", "Ms.", "Miss", "Aunt", "Uncle", "Mr. and Mrs."] # We are creating a list of titles
    for character in new_characters: # We are iterating over the characters in the list
        if "" != character: # We are checking if the character is not an empty string
            final_characters.append(character) # We are adding the character to the list
            for title in titles: # We are iterating over the titles in the list
                titled_char = f"{title} {character}" # We are combining the title and character
                final_characters.append(titled_char) # We are adding the titled character to the list


    print (len(final_characters)) # We are printing the number of items in the list
    final_characters = list(set(final_characters)) # We are removing any duplicates from the list
    print (len(final_characters)) # We are printing the number of items in the list
    final_characters.sort() # We are sorting the list
    return (final_characters) # We are returning the list

#  Now we need to create the training data for the custom NER model. We can define a function to do this for us
def create_training_data(file, type): # This function will create the training data for the custom NER model
    data = generate_better_characters(file) # We are generating a list of characters from the Harry Potter series
    patterns = [] # We are creating an empty list to store the patterns
    for item in data: # We are iterating over the items in the data
        pattern = { # We are creating a dictionary to store the pattern
                    "label": type, # We are assigning the type to the label
                    "pattern": item # We are assigning the item to the pattern
                    }
        patterns.append(pattern) # We are adding the pattern to the list
    return (patterns) # We are returning the list

#  Now we need to generate the rules for the custom NER model. We can define a function to do this for us
def generate_rules(patterns): # This function will generate the rules for the custom NER model
    nlp = English() # We are loading the English language model
    ruler = EntityRuler(nlp) # We are creating an EntityRuler object
    ruler.add_patterns(patterns) # We are adding the patterns to the EntityRuler object
    # nlp.add_pipe(ruler) # We are adding the EntityRuler object to the pipeline
    nlp.add_pipe('entity_ruler')
    nlp.get_pipe('entity_ruler').add_patterns(patterns)
    nlp.to_disk("hp_ner") # We are saving the custom NER model to disk


def test_model(model, text): # This function will test the custom NER model
    doc = nlp(text) # We are processing the text with the model
    results = [] # We are creating an empty list to store the results
    for ent in doc.ents: # We are iterating over the entities in the document
        results.append(ent.text) # We are adding the entity text to the list
    return (results) # We are returning the list

patterns = create_training_data("data/hp_characters.json", "PERSON") # We are creating the training data for the custom NER model
generate_rules(patterns) # We are generating the rules for the custom NER model
# print (patterns)

# Now we need to test the custom NER model.
# First we need to load the custom NER model.
nlp = spacy.load("hp_ner") # We are loading the custom NER model

# Next we need to test the custom NER model.
ie_data = {} # We are creating an empty dictionary to store the data

with open ("data/hp.txt", "r")as f: # We are opening the file in read mode
    text = f.read() # We are reading the text from the file

    # We are splitting the text into chapters
    chapters = text.split("CHAPTER")[1:] # We are splitting the text into chapters
    for chapter in chapters: # We are iterating over the chapters
        chapter_num, chapter_title = chapter.split("\n\n")[0:2] # We are splitting the chapter into the chapter number and title
        chapter_num = chapter_num.strip() # We are removing any leading or trailing whitespace from the chapter number
        segments = chapter.split("\n\n")[2:] # We are splitting the chapter into segments
        hits = [] # We are creating an empty list to store the hits
        for segment in segments: # We are iterating over the segments
            segment = segment.strip() # We are removing any leading or trailing whitespace from the segment
            segment = segment.replace("\n", " ") # We are replacing newlines with spaces
            results = test_model(nlp, segment)  # We are testing the custom NER model
            for result in results:  # We are iterating over the results
                hits.append(result) # We are adding the result to the list
        ie_data[chapter_num] = hits # We are adding the hits to the dictionary

save_data("data/hp_data_GG.json", ie_data) # We are saving the data to a JSON file

#  Now we need to evaluate the custom NER model. We can define a function to do this for us
def evaluate_model(file): # This function will evaluate the custom NER model
    data = load_data(file) # We are loading the data from the file
    total = 0 # We are initializing the total variable
    correct = 0 # We are initializing the correct variable
    for chapter in data: # We are iterating over the chapters in the data
        total += len(data[chapter]) # We are incrementing the total variable
        for item in data[chapter]: # We are iterating over the items in the chapter
            if item in chapter: # We are checking if the item is in the chapter
                correct += 1 # We are incrementing the correct variable
    accuracy = correct / total # We are calculating the accuracy
    return (accuracy) # We are returning the accuracy

accuracy = evaluate_model("data/hp_data_GG.json") # We are evaluating the custom NER model
print (f"Accuracy: {accuracy}") # We are printing the accuracy


# We can test the model on a made up sentence, and see if it detects entities

test = "Mr. Dursley was the director of a firm called Grunnings, which made drills. He was married to Petunia. They had a son named Dudley. They lived at number four, Privet Drive."

doc = nlp(test) # We are processing the text with the model
for ent in doc.ents: # We are iterating over the entities in the document
    print (ent.text, ent.label_) # We are printing the entity text and label


