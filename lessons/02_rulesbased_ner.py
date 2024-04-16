#   NAMED ENTITY RECOGNITION SERIES   #
#             Lesson 02               #
#          Rules-Based NER            #
#               with                  #
#        Dr. W.J.B. Mattingly         #
import json

# Here we are going to use the Harry Potter text to find the characters in the text.
# We will use the list of characters from the JSON file to find the characters in the text.
# We will then print out the characters we find in the text.

# First, we will open the Harry Potter text file and read the text into a list of segments.
with open ("data/hp.txt", "r", encoding="utf-8") as f:
    text = f.read().split("\n\n")
    # print (text)

# Next, we will open the JSON file with the list of Harry Potter characters.
character_names = [] # create an empty list to store the character names
with open("data/hp_characters.json", "r", encoding="utf-8") as f: # open the JSON file
    characters = json.load(f)   # load the JSON file
    for character in characters: # for each character in the JSON file
        names  = character.split() # split the character name into a list of words
        for name in names: # for each word in the character name
            if "and" != name and "the" != name and "The" != name: # if the word is not "and" or "the" or "The"
                name = name.replace(",", "").strip() # remove any commas and white spaces
                character_names.append(name) # add the word to the list of character names

# print (character_names)

# Now we will iterate through the text segments and find the characters in the text.
for segment in text: # for each segment in the text
    # print (segment)
    segment = segment.strip() # remove any leading or trailing white spaces
    segment = segment.replace("\n", " ") # replace any new lines with a space
    print (segment) # print the segment

    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~''' # create a string of punctuation marks
    for ele in segment: # for each character in the segment
        if ele in punc: # if the character is a punctuation mark
            segment = segment.replace(ele, "") # remove the punctuation mark
    # print (segment)
    words = segment.split() # split the segment into a list of words
    # print (words)
    i = 0 # create a counter variable
    for word in words: # for each word in the segment
        if word in character_names: # if the word is in the list of character names
            if words[i-1][0].isupper(): # if the previous word is capitalized
                print (f"Found Character(s): {words[i-1]} {word}") # print the previous word and the current word
            else: # otherwise
                print (f"Found Character(s): {word}") # print the current word

        i=i+1 # increment the counter variable
