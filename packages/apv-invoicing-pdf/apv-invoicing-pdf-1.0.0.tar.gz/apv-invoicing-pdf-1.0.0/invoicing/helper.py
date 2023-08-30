import os

# * * * * * * *   G L O B A L   V A R I A B L E S   * * * * * * * #
WORKING_DIR = '/Volumes/EVO1T/OneDrive/Tutorials/2.Active/Learn Python in 50 Days/Apps/App04/'


# * * * * * * * * * * *  F U N C T I O N S   * * * * * * * * * * * #

# set the working directory
def setWorkingDirectory(root_path:str=WORKING_DIR):
    os.chdir(root_path)
