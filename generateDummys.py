import os
import random
import string

def generate_random_string():
    # Generate a random length between 2 and 15
    length = random.randint(2, 15)
    
    # Generate a string of all possible characters except the ones that can mess up a path
    characters = string.ascii_letters + string.digits + "_- "
    
    # Use random.sample to select 'length' number of characters from the string
    random_string = ''.join(random.sample(characters, length))
    
    return random_string


# Prompt the user for the number of files to create
num_files = int(input("How many files do you want to create? "))

# Specify the format of the filename
prefix = "dummyfiles/"
suffix = ".dummy"

# Create the files
for i in range(1, num_files + 1):
    # Increment the number at the end of the filename
    filename = prefix + generate_random_string()+ "_" +str(i).zfill(3) + suffix
    
    # Create an empty file with the specified filename
    with open(filename, "w") as file:
        pass
    
    # Print a message to indicate that the file has been created
    print("Created file:", filename)
