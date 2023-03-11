#!/usr/bin/env python

'''
Git RepoMaker

Set up your Python project on GitHub with an easy to use front end.  
Simply create your project project, add the python files and then run this 
script in order to create the rest of the configuration files.
- Git files
- requirements.txt
- Boilerplate README.md with installation and update instructions
'''

import subprocess
import time

print("Welcome to Git RepoMaker.")
print("-" * 30)
print("")
print("Let's set up the GitHub repository first." 
time.sleep(2)

# Define the parameters
git_name = ''
git_email = ''
git_commit = ''
git_token = ''
repo_title = ''
project_dir = ''
project_main = ''
project_descr = ''
project_features = ''

while git_name in "":
    git_name = input("Enter your GitHub user name: ")

while git_email in "":
    git_email = input("Enter your GitHub user email: ")

while git_commit in "":
    git_commit = input("Enter your commit comments (eg. 'First commit'): ")

print("Paste your personal access token. NOTE: This token is not saved but simply passed directly to GitHub.\nIf you don't have a token, take a look here before continuing:\n https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token"

while git_token in "":
    git_token = input("> ")
    
print("Repository successfully created. Now let's define a few things about our project. Ready?")

while project_title in "":
    project_title = input("Enter project title: ")

while project_dir in "":
    project_dir = input("Enter project local directory (full path): ")

while project_main in "":
    project_main = input("Enter project main .py file: ")

print("Write a few words about the project. Markdown is fully supported. \n# | ## | ### = Header 1 | Header 2 | Header 3 \n[descr](link) | * Bullet point | *Italics | **Bold \n")

project_descr = []
# Allow multiline input
while True:  
    line = input("> ")
    if line:
        line = line + " \n"
        project_descr.append(line)
    else:
        break
    
print("Enter project features, one per line.")

project_features = []
while True:  
    line = input("> ")
    if line:
        line = "* " + line + " \n"
        project_features.append(line)
    else:
        break
