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
print("Let's set up the GitHub repository first...")
time.sleep(2)

# Define the parameters
git_user = ''
git_email = ''
git_commit = ''
git_token = ''
repo_name = ''
repo_descr = ''
project_title = ''
project_dir = ''
project_main = ''
project_descr = ''
project_features = ''

while project_dir in "":
    project_dir = input("Enter project local directory (full path): ")

while git_user in "":
    git_user = input("Enter your GitHub user name: ")

while git_email in "":
    git_email = input("Enter your GitHub user email: ")

while git_commit in "":
    git_commit = input("Enter your commit comments (eg. 'First commit'): ")

print("Paste your personal access token. NOTE: This token is not saved but simply passed directly to GitHub.\nIf you don't have a token, take a look here before continuing:\n https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token")

while git_token in "":
    git_token = input("> ")
    
print("\nNow let's define a few things about our project...")
time.sleep(2)

while project_title in "":
    project_title = input("Enter project title: ")
    # Use title to create repository name
    repo_name = project_title.title().replace(" ", "")

while repo_descr in "":
    repo_descr = input("Enter one line description: ")

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


# Curl command for creating the new repository on GitHub

new_repo = "curl -L -X POST -H \"Accept: application/vnd.github+json\" -H \"Authorization: Bearer " + git_token + "\" -H \"X-GitHub-Api-Version: 2022-11-28\" https://api.github.com/user/repos -d '{\"name\":\"" + repo_name + "\",\"description\":\"" + repo_descr + "\",\"homepage\":\"https://github.com\",\"private\":false,\"is_template\":true}'"


# Create the README.md

file0 = open("README.md", "w")
txt = f"""# {project_title}
![Screenshot](screenshot.png)

{project_descr}

### Features
{project_features}

### Installation and Updating
1. Create a folder for the application (eg. `{project_dir}`).
2. Install all required dependencies.

       python3 -m pip install -r requirements.txt

3. Run in a terminal:

       cd {project_dir}
       git clone https://github.com/{git_user}/{repo_name}.git --branch master

### Update
In order to update the application, open a terminal and run:

    cd {project_dir}
    git pull

## Usage
Go to the application's folder and run:

```
python3 {project_main}.py
```

or if you are in Windows enter:

```
c:\python<PYTHON_VERSION_HERE>\python.exe {project_main}.py
```

"""
file0.writelines(txt)
file0.close()


# Run system commands

print("Project files created. Running system commands and wrapping up.")
time.sleep(2)

subprocess.run(['cd', project_dir])
subprocess.run(['pipreqs'])
subprocess.run(['git', 'config', '--local', 'user.name', '"' + git_user + '"'])
subprocess.run(['git', 'config', '--local', 'user.email', '"' + git_email + '"'])
subprocess.run(['git', 'init'])
subprocess.run(['git', 'add', '.'])
subprocess.run(['git', 'commit', '-m', git_commit])
subprocess.run(new_repo)
subprocess.run(['git', 'push', 'origin', 'master'])

print(f"Project repository created at https://github.com/{git_user}/{repo_name}.git")
print("Enjoy!")
