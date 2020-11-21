# Steps
1. Install the last versions of browsers: "Chrome", "Firefox";
2. Download the latest versions of webdrivers: "chromedrive", "geckodriver";
3. Install "python 3X";
4. Add path to webdrivers, "\ python3X \", "\ python3X \ Scripts \" into the environment variable: "Path";
5. Using "pip" in the command console, install packages and libraries from the file: "packages.txt":
    ```
    cd "path to packages.txt"
    python -m pip install -r packages.txt
    ```
6. Download the test project from the git-repository;
7. Open the project in "PyCharm";
8. Create "Run \ Debug Configuration":
    - Add "Python tests" -> "pytest";
	- Determine the "Script path" to the test case file: "test_twitter.py";
	- Add "--alluredir ./results" to "Additional Arguments";
	- Project supports additional arguments: 
        ```
        --cmd_opt_browser_name chrome --cmd_opt_username_email test@gmail.com 
	    --cmd_opt_username testusername --cmd_opt_password testpassword
        ```
9. Start the test;
10. An JSON files will be created in the "results" folder;

## Optional
11. Setup the allure server: https://docs.qameta.io/allure/#_windows
12. Build a report by command: 
    ```
    allure serve "path_to\results"
    ```
