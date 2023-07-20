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

import re, io, os
import webbrowser
import PySimpleGUI as sg
import subprocess
from PIL import Image
from random import choice
from time import sleep


def compiler():
    print('Creating boilerplate README.md...')
    window.refresh()
    sleep(1)    
    file0 = open('README.md', 'w')
    txt = f"""# {gui.title}
![Screenshot](screenshot.png)

{gui.details}

### Features
{gui.features}

### Installation and Updating
1. Create a folder for the application (eg. `{gui.sample_path}`).
2. Install all required dependencies.

        python3 -m pip install -r requirements.txt

3. Run in a terminal:

        cd {gui.sample_path}
        git clone https://github.com/{gui.username}/{gui.repo_name}.git --branch master

### Update
In order to update the application, open a terminal and run:

    cd {gui.sample_path}
    git pull

## Usage
Go to the application's folder and run:

```
python3 {gui.project_file}
```

or if you are in Windows enter:

```
c:\python<PYTHON_VERSION_HERE>\python.exe {gui.project_file}
```

"""
    file0.writelines(txt)
    file0.close()

    # Run system commands
    print('Project files created.') 
    
    try:
        print('Running system commands.')
        sleep(1)
        cmd('cd ' + gui.project_path)
        cmd('pipreqs')
        cmd('git init')
        cmd('git config --local user.name ' + '"' + gui.username + '"')
        cmd('git config --local user.email ' + '"' + gui.usermail + '"')
        cmd('git add .')
        cmd('git commit -m "' + gui.commit + '"')
        print('Creating GitHub repository...')
        print('*** If execution is suspended, check Terminal for user input request. ***')
        print('*** If Git prompts you for your password, enter your personal access token. ***') 
        window.refresh()
        sleep(1)
        cmd('git remote add origin https://github.com/' + gui.username + '/' + gui.repo_name + '.git')
        cmd(gui.new_repo)
        cmd('git push origin master')
    except:
        print('Compilation error.')
        print('OSError > ',e.filename)
        print('OSError > ',e.strerror)
        sg.Popup('Oops! Compilation error. Please check the values and try again.')
 
def typewriter(text):
    # Fun little typewriter effect for the terminal window - Unused
    for i in text:
        print(i, end = '', flush = True)
        sleep(0.03)

def cmd(var):
    # Small function to handle running shell commands
    result = subprocess.run([var], shell=True, capture_output=True, text=True, check=False)
    print(result.stdout)
    print(result.stderr)
    
def gui():
    # Create the graphical interface
    ver = 'v1.45'
    gui.buffer = '.repo_data'
    url = 'https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token'    
    
    col1 = sg.Column([
                [sg.HorizontalSeparator()],
                [sg.T('GitRepoMaker - Create GitHub Repositories', font='_ 22 bold'), sg.Push(),
                 sg.Image(sg.EMOJI_BASE64_DREAMING)],
                
                [sg.Frame(' GitHub Configuration ', 
                [sg.vtop(
                [sg.Column([
                [sg.T('User name ', s=14), sg.In(key='-USERNAME-', s=25)], 
                [sg.T('User email', s=14), sg.In(key='-USERMAIL-', s=25, enable_events=True)],
                [sg.T('Screenshot', s=14), sg.In(key='-SCRSHOT-', s=40, enable_events=True), 
                sg.FileBrowse(file_types=[('*.jpg', '*.png')])],
                [sg.T('Access Token', s=14), sg.In(key='-TOKEN-', s=40)]]), 
                
                sg.Column([
                [sg.Image(key='!IMAGE!', s=(96,64), background_color='#4F5D7A')]])]), 
                [sg.T('NOTE: This token is not saved locally. If you don\'t have a token yet, create it here:'),
                sg.T('https://www.github.com', font='_ 11 underline', text_color='Blue', enable_events=True, key='!URL!')]
                ], expand_x=True)],

                [sg.Frame(' Project Information ', [
                [sg.T('Project Title', s=14), sg.In(key='-TITLE-', s=40, enable_events=True)], 
                [sg.T('Short Description', s=14), sg.In(key='-DESCR-', s=57)], 
                [sg.T('Commit comments', s=14), sg.In(key='-COMMIT-', s=57)],
                [sg.T('App example path', s=14), sg.In(key='-PATH1-', s=30, enable_events=True), 
                 sg.T('App exec'), sg.In(key='-PATH2-', s=16, enable_events=True), 
                sg.FileBrowse()],
                [sg.T('Details (README.md)\nMarkdown is fully supported. \n![img](img.png)\n[descr](link)\n *Italics\n **Bold', s=(14,8)), sg.Multiline(key='-DETAILS-', border_width=0, no_scrollbar=True, s=(60,8), expand_x=True)], 
                [sg.T('Main Features\n * Bullet points', s=(14,4)), sg.Multiline(key='-FEATURES-', border_width=0, no_scrollbar=True, s=(60,6), expand_x=True)]
                ], expand_x=True)],
                 
                [sg.HorizontalSeparator()],
                [sg.Button('Read', s=(10)), sg.Button('Write', s=(10)), sg.Button('Clear', s=(10)), sg.Button('COMPILE', expand_x=True, button_color = '#006600'), sg.Button('Exit', s=(10), button_color = '#000')],
                [sg.StatusBar('', key='Status', s=40)]
                ])
                
    col2 = sg.Column([
                [sg.Output(size=(60, 50), background_color='black', text_color='white', font='Courier 10', sbar_trough_color = 'black', sbar_background_color = 'black', sbar_arrow_color = 'black', sbar_width = 0, sbar_arrow_width = 0, key='!OUT!', expand_y=True, expand_x=True)],
                [sg.Push(), sg.T('Made with'), sg.Image('res/love.png'), sg.T('and'), sg.Image('res/coffee.png'), sg.T(' | ' + ver), sg.Push()],
                [sg.Push(), sg.T(quote(), s=(60,3), justification='center'), sg.Push()]
                ])
    
    layout = [sg.vtop([col1, col2])]
    
    global window  # Ugly but needed to define the window variable outside of the function
    window = sg.Window('GitHub RepoMaker ' + ver, layout, font='_ 11', resizable=False)
    
    prompt = window['Status'].update
    
    # Create dictionary with all input objects.
    input_key_list = [key for key, value in window.key_dict.items()
    if isinstance(value, sg.In)]
    
    while True:   
        event, values = window.read(timeout=250)
        
        try:
            for key, value in window.key_dict.items():
                if isinstance(value, sg.In):
                    # Make sure we have a properly formatted email address
                    if not re.match(r'[^@]+@[^@]+\.[^@]+', values['-USERMAIL-']):
                        window['-USERMAIL-'].update(background_color='#FFCCCC')
                    # Check if fields are filled in and colour accordingly
                    elif values[key] != '':
                        window[key].update(background_color='#CCFFCC')
                    else:
                        window[key].update(background_color='#FFFFFF')
                        
            if event == sg.WIN_CLOSED or event == 'Exit':
                if sg.Window('Warning', [[sg.Text('Do you want to quit?')], 
                    [sg.Yes(s=10), sg.No(s=10)]], keep_on_top=True).read(close=True)[0] == 'Yes':
                    break
                else:
                    pass
            elif event == '-SCRSHOT-':
                filename = values['-SCRSHOT-']
                if os.path.exists(filename):
                    try:
                        image = Image.open(filename)
                        image.thumbnail((600, 400), Image.Resampling.LANCZOS)
                        bio = io.BytesIO()
                        image.save(bio, format='PNG')
                        window['!IMAGE!'].update(data=bio.getvalue(), subsample=5)
                    except:
                        window['!IMAGE!'].update(source=None)
                        sg.Popup('Error: Selected file is not a valid image.', title = 'Warning')
                        pass                        
            elif event == '-TITLE-' and values['-TITLE-'] != '':
                if os.name == 'nt':
                    gui.sample_path = 'c:\\' + values['-TITLE-'].replace(' ', '_')
                else:
                    gui.sample_path = '~/' + values['-TITLE-'].replace(' ', '_')
                window['-PATH1-'].update(gui.sample_path)
            elif event == '-PATH2-' and '/' or '\\' in values['-PATH2-']:
                try: 
                    try:
                        if os.name == 'nt':
                            os_path = values['-PATH2-'].rsplit('\\', 1)
                            image.save(os_path[0] + '\\screenshot.png', format='PNG')
                        else:
                            os_path = (values['-PATH2-'].replace(' ', '\ ')).rsplit('/', 1)
                            image.save(os_path[0] + '/screenshot.png', format='PNG')
                    except:
                        pass
                    window['-PATH2-'].update(os_path[1])
                except IndexError:
                    pass
            elif event  == '!URL!':
                print('Opening GitHub Docs page...')
                webbrowser.open(url)
            elif event  == 'Clear':
                if sg.Window('Warning', [[sg.Text('Do you want to clear all values?')], 
                    [sg.Yes(s=10), sg.No(s=10)]], keep_on_top=True).read(close=True)[0] == 'Yes':
                    prompt('Clearing all input fields.')
                    window['-USERNAME-'].update('')
                    window['-USERMAIL-'].update('')
                    window['-SCRSHOT-'].update('')
                    window['-TOKEN-'].update('')
                    window['-TITLE-'].update('')
                    window['-DESCR-'].update('')
                    window['-COMMIT-'].update('')
                    window['-PATH1-'].update('')
                    window['-PATH2-'].update('')
                    window['-DETAILS-'].update('')
                    window['-FEATURES-'].update('')
                else:
                    prompt('')
                    pass
            elif event  == 'Write':
                # Check if fields are blank or not.
                if not any(map(str.strip, [values[key] for key in input_key_list])):
                    prompt('Fields are empty. Nothing to write.')
                else:
                    prompt('Saving input fields...')
                    tempfile = open(gui.buffer, 'w')
                    for key, value in window.key_dict.items():
                        if isinstance(key, str) and key.startswith('-TOK'):
                            tempfile.write('±±')
                        elif isinstance(key, str) and key.startswith('-'):
                            tempfile.write(values[key] + '±±')
                        elif isinstance(key, str) and key.startswith('-DET'):
                            tempfile.write(value[key] + '±±')
                        elif isinstance(key, str) and key.startswith('-FEAT'):
                            tempfile.write(value[key] + '±±')
                    tempfile.close()
                    sleep(1)
                    prompt('Saving input fields... Done.')
            elif event == 'Read':
                try:
                    tempfile = open(gui.buffer, 'r')
                    t = tempfile.read().split('±±')
                    if t == ['']:
                        pass
                    else:
                        prompt('Reading input fields...')
                        window['-USERNAME-'].update(t[0])
                        window['-USERMAIL-'].update(t[1])
                        window['-SCRSHOT-'].update(t[2])
                        window['-TOKEN-'].update(t[3])
                        window['-TITLE-'].update(t[4])
                        window['-DESCR-'].update(t[5])
                        window['-COMMIT-'].update(t[6])
                        window['-PATH1-'].update(t[7])
                        window['-PATH2-'].update(t[8])
                        window['-DETAILS-'].update(t[9])
                        window['-FEATURES-'].update(t[10])
                        tempfile.close()
                        try:
                            if os.name == 'nt':
                                os_path = t[2].rsplit('\\', 1)
                            else:
                                os_path = (t[2].replace(' ', '\ ')).rsplit('/', 1)
                        except:
                            pass
                        sleep(1)
                        prompt('Reading input fields... Done.')                        
                except:
                    tempfile = open(gui.buffer, 'w')
                    tempfile.close()
                    pass
            elif event == 'COMPILE':
                if values['-USERMAIL-'].find('@') <= 0:
                    window['-USERMAIL-'].update(background_color='#FFCCCC')
                    prompt('This is not a valid email address')
                else:
                    window['-USERMAIL-'].update(background_color='#FFFFFF')
                    prompt('This is a valid email address')
                
                if all(map(str.strip, [values[key] for key in input_key_list])):
                    prompt('All input fields are OK. Compiling...')
                    window.refresh()
                    sleep(1)
                    print('Running new repository compiler.')
                    window.refresh()
                    sleep(1)
                    print('-' * 30)
                    window.refresh()
                    print('')
                    print('Initializing project parameters...')
                    window.refresh()
                    sleep(1)
                    gui.username = values['-USERNAME-']
                    gui.usermail = values['-USERMAIL-']
                    gui.screenshot = values['-SCRSHOT-']
                    gui.token = values['-TOKEN-']
                    gui.title = values['-TITLE-']
                    gui.descript = values['-DESCR-']
                    gui.commit = values['-COMMIT-']
                    gui.details = values['-DETAILS-']
                    gui.features = values['-FEATURES-']
                    if os.name == 'nt':
                        gui.sample_path = 'c:\\' + values['-TITLE-'].replace(' ', '_')
                    else:
                        gui.sample_path = '~/' + values['-TITLE-'].replace(' ', '_')
                        
                    print('Sanitizing input values...')
                    window.refresh()
                    sleep(1)
                    
                    # Sanitize project title and reformat as per GitHub
                    # (remove whitespaces, extra and non unicode chars etc)
                    rn = gui.title.replace(' ', '-')
                    rn = re.sub('[^A-Za-z0-9 ]+', '-', rn)
                    gui.repo_name = rn.replace(' ', '')
                    
                    # Specify files to omit via .gitignore.
                    with open('.gitignore', 'w') as f:
                        f.write('.repo_data\n.DS_Store')

                    # Pass os_path values outside of the fuction and construct the new repo curl
                    gui.project_path = os_path[0] 
                    gui.project_file = os_path[1]
                    gui.new_repo = "curl -L -X POST -H \"Accept: application/vnd.github+json\" -H \"Authorization: Bearer " + gui.token + "\" -H \"X-GitHub-Api-Version: 2022-11-28\" https://api.github.com/user/repos -d '{\"name\":\"" + gui.repo_name + "\",\"description\":\"" + gui.descript + "\",\"homepage\":\"https://github.com\",\"private\":false,\"is_template\":false}'"
                    
                    compiler()
                else:
                    prompt('Some input fields are blank.')       
                    
        except RuntimeError as e:
            prompt('Compilation error.')
            sg.Popup('Oops! Compilation error. ' + e, title = 'Warning')
        
    window.close()

def quote():
    quotes_list = ['The best thing about a boolean is even if you are wrong, you are only off by a bit. (Anonymous)', 'Without requirements or design, programming is the art of adding bugs to an empty text file. (Louis Srygley)', 'Before software can be reusable it first has to be usable. (Ralph Johnson)', 'The best method for accelerating a computer is the one that boosts it by 9.8 m/s2. (Anonymous)', 'I think Microsoft named .Net so it wouldn’t show up in a Unix directory listing. (Oktal)', 'There are two ways to write error-free programs; only the third one works. (Alan J. Perlis)', 'It’s not a bug – it’s an undocumented feature. (Anonymous)', 'One man’s crappy software is another man’s full-time job. (Jessica Gaston)', 'A good programmer is someone who always looks both ways before crossing a one-way street. (Doug Linder)', 'Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live. (Martin Golding)', 'Programming is like sex. One mistake and you have to support it for the rest of your life. (Michael Sinz)', 'Deleted code is debugged code. (Jeff Sickel)', 'If debugging is the process of removing software bugs, then programming must be the process of putting them in. (Edsger Dijkstra)', 'Software undergoes beta testing shortly before it’s released. Beta is Latin for “still doesn’t work. (Anonymous)', 'Programming today is a race between software engineers striving to build bigger and better idiot-proof programs, and the universe trying to produce bigger and better idiots. So far, the universe is winning. (Rick Cook)', 'There are only two kinds of programming languages: those people always bitch about and those nobody uses. (Bjarne Stroustrup)']
    
    return choice(quotes_list)
    
if __name__ == '__main__':
    gui()
