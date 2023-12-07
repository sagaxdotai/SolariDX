# Steps for a Successful EC2 Work Session

Step 1: Get the current DNS host name.

Step 2: Add the host name to the "config" file in your .ssh folder.

Step 3: Open VS Code and click the icon in the bottom left corner.

Step 4: Select "Connect to Host..." in the popup that opens.

Step 5: Click on the host from your .ssh file. A new VS Code window should open (you may have to click "Continue" on a second popup menu).

Step 6: In the new window, open a VS Code terminal (```ctrl + ~```), and type
```
./start_QCuda_[yourname]
```
This will launch your docker instance and populate it with your code from GitHub.

Step 7: Edit and run your code as needed. Be sure to make all your changes in your personal folder. To open your folder in your terminal, type:
```
cd [yourname]
```
To open your files in VS Code, do the following:

1. Click the Docker (whale) icon in the far left sidebar.

2. Locate the "CONTAINERS" dropdown at the top of the secondary left sidebar.

3. Click on the following dropdown arrows:

> "Individual Containers" -> "nvcr.io/nvidia/cuda-quantum:0.4.1" -> "Files" -> "home" -> "cudaq" -> [yourname]

4. Hover over the file you want to open and click on the page icon to open it.

5. Edit the file and remember to save!

6. To run a python file, in the terminal type:
```
python [filename].py
```

Step 8: When you have finished your work, in the terminal type
```
exit
```

Step 9: Now save you changes and close your instance using
```
./save_QCuda_[yourname]
```

Step 10: Click the icon in the bottom left corner and select "Close Remote Connection" in the popup that opens.
