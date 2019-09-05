import easygui
import os
import hashlib
import tkinter as tk

dir_path = easygui.diropenbox("")  # get directory path from user

files = os.listdir(dir_path)
#print(files)

# filter out only files. We dont want folders
files = ( file for file in files if os.path.isfile( path=os.path.join(dir_path, file) ) )

# sort these files according to access time. https://unix.stackexchange.com/a/2465/218439
files = sorted(files, key=lambda fn: os.path.getatime(os.path.join(dir_path, fn)))
#print(files)

hash_table = dict()    # dictionary that matches filename against hash of its content
duplicates = []        # list of duplicate filepaths
for filename in files:
    filepath = os.path.join(dir_path, filename)

    with open(filepath, 'rb') as filepointer: # open file as read in binary format
        content = filepointer.read() # binary content of string(path)
    

    hasher = hashlib.sha256()    # create a SHA256 hasher
    hasher.update(content)       # pipe file content through the hasher
    print(hasher, end = " ")
    _hash = hasher.hexdigest()   # get the hash of the content
    print(_hash, end = " ")

    if _hash in hash_table.keys():  # if hash already exists, we found a duplicate
        #print(filepath)
        duplicates.append(filepath) 
    else:
        hash_table[_hash] = filepath
        #print(hash_table)

# Ask user for each duplicate if it can be deleted and upon ACK, delete it.
for dup in duplicates:
    filename = os.path.split(dup)[1]  # get filename from filepath
    print(filepath)
    choice = easygui.choicebox(title="Delete Duplicate?", msg="Can i Delete {FILENAME}?".format(FILENAME=filename), choices=['delete', 'ignore'])
    if choice == 'delete':
        os.remove(dup)