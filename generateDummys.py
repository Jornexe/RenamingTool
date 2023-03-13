import os

# Prompt the user for the number of files to create
num_files = int(input("How many files do you want to create? "))

# Specify the format of the filename
prefix = "dummyfiles/_"
suffix = ".dummy"

# Create the files
for i in range(1, num_files + 1):
    # Increment the number at the end of the filename
    filename = prefix + str(i).zfill(3) + suffix
    
    # Create an empty file with the specified filename
    with open(filename, "w") as file:
        pass
    
    # Print a message to indicate that the file has been created
    print("Created file:", filename)
