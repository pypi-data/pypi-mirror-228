def debugChecks_main(self):
    try:
        # check if "TracerPid" is enabled
        if "TracerPid" in self.anti_debug_checks:
            # TracerPid is enabled run check
            if TracerPidCheck(self):return True

        # check if "WindowNames" is enabled
        if "WindowNames" in self.anti_debug_checks:
            # WindowNames is enabled run check
            if WindowNamesCheck(self):return True

        # check if "ProcessNames" is enabled
        if "ProcessNames" in self.anti_debug_checks:
            # ProcessNames is enabled run check
            if ProcessNamesCheck(self):return True

    except Exception as e:
        if self.debug is True:
            raise e
        else:pass


import pygetwindow as gw
import psutil
import os
# lists
from .lists.default_debugCheck import *


def TracerPidCheck(self):
    # Check for the presence of the tracerpid file in /proc/self/
    tracerpid_path = "/proc/self/status"
    if os.path.exists(tracerpid_path):
        with open(tracerpid_path, "r") as status_file:
            status_content = status_file.read()
            if "TracerPid:\t0" not in status_content:
                # Debugger detected
                return True
    # No debugger detected
    return False


def WindowNamesCheck(self):
    # Get all open window names
    window_names = gw.getAllTitles()

    # Check if one window name is in the blacklisted window title list
    for window_name in window_names:
        # check what list to take default or user-specified
        if self.anti_debug_custom_lists["windowNames"] is None:
            # default list
            if window_name in default_windowNames_list:
                # blacklisted window open
                return True
        else:
            user_windowNames_list = self.anti_debug_custom_lists["windowNames"]
            # user/custom list
            if window_name in user_windowNames_list:
                # blacklisted window open
                return True
    # No blacklisted window open
    window_names.clear()
    return False


def ProcessNamesCheck(self):
    process_names = []
     
    # get all open process names
    for p in psutil.process_iter(attrs=['name']):
        process_names.append(p.info['name'])

    # Check if one process name is in the blacklisted process name list
    for process_name in process_names:
        # check what list to take default or user-specified
        if self.anti_debug_custom_lists["ProcessNames"] is None:
            # default list
            if process_name in default_processNames_list:
                # blacklisted process open
                return True  
        else:
            user_processNames_list = self.anti_debug_custom_lists["ProcessNames"]
            # user/custom list
            if process_name in user_processNames_list:
                # blacklisted process open
                return True
    # No blacklisted process open
    process_names.clear()
    return False