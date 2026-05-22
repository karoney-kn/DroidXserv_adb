import os
import sys
import subprocess
import platform


#-------------------------------------------------------------------------#

################################ ToolKit Section ##############################

#-------------------------------------------------------------------------#


def start():
    try:
        
        os.makedirs("./config/media-files")
        os.makedirs("./config/sys_logs")
        os.makedirs("./config/json_files")
    except:
        pass


def sf_spacing(content: str):
    tabbed_content = '\n\t'.join(line.lstrip() for line in content.splitlines())
    return tabbed_content

