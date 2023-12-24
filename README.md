# Python Testing Suit 2.0
## What is it?
It is simple browser powered system for testing python programs.
## General purpose
General purpose is education in schools or colleges.
## abilities
Writing problems which will be able to be solved in python 3
## How to use it?
Just run main.py and after should be opened your browser with catalog of tasks. Click on required task, next you will see page with description of task and text area for code. Just write solution in python into this text area and click on "Check Solution". in block at bottom will appear text "OK" if solution is right, "FAIL" if it is wrong and "ERROR" if server got an exception. 
## What if I want to make a link to required task (on desktop, for example)?
copy code below and paste link to task instead of `<task_link>`, next paste it into link path (for Windows)
```
py %CURRENTUSER%/AppData/pts2/server.py & <task_link>
```

for linux, copy code below, replace link and create on desktop file `"TaskName.desktop"`

```
[Desktop Entry]
Type=Application
Name=TaskName
Exec=python3 ~/.pts2/server.py & <task_link>
Terminal=false
Icon=~/.icons/pts2task.png
```
