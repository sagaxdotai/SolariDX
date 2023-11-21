# Steps for a Successful EC2 Work Session

Step 1: Get the current DNS host name.

Step 2: Add the host name to the "config" file in your .ssh folder.

Step 3: Open VS Code and click the green icon in the bottom left corner.

Step 4: Select "Connect to Host..." in the popup that opens.

Step 5: Click on the host from your .ssh file. A new VS Code window should open.

Step 6: Open a VS Code terminal (```ctrl + ~```), and type
```
./Start_QCuda_[yourname]
```
This will launch your docker instance and populate it with your code from GitHub.

Step 7: Edit and run your code as needed. To run a file, type
```
nvq++ path/to/file/file_name.cpp
./a.out
```

Step 8: When you have finished your work, type
```
exit
```

Step 9: Now save you changes and close your instance using
```
./Save_QCuda_[yourname]
```

