def vmChecks_main(self):
    try:
        # check if "KnownIps" is enabled
        if "KnownIps" in self.anti_vm_checks:
            #  is enabled run check
            if KnownIpsCheck(self):return True

        # check if "VMPaths" is enabled
        if "VMPaths" in self.anti_vm_checks:
            # is enabled run check
            if vmPathsCheck(self):return True

        # check if "ProcessNames" is enabled
        if "ProcessNames" in self.anti_vm_checks:
            # is enabled run check
            if ProcessNamesCheck(self):return True

        # check if "ManufactureRelease" is enabled
        if "ManufactureRelease" in self.anti_vm_checks:
            # is enabled run check
            if ManufactureReleaseCheck(self):return True

    except Exception as e:
        if self.debug is True:
            raise e
        else:pass


import urllib.request
import platform
import psutil
import os
# lists
from lists.default_vmCheck import *



def KnownIpsCheck(self):
    # get public IP (ipv4)
    computer_ip = urllib.request.urlopen('http://4.tnedi.me').read().decode('utf8')
    # check if ip is empty if yes dont check
    if computer_ip is None:
        return False
    
    # check if ip is blacklisted
    # check what list to take default or user-specified
    if self.anti_vm_custom_lists["knownIps"] is None:
        # default list
        if computer_ip in default_knownIps_list:
            # blacklisted ip
            return True  
    else:
        user_knownIps_list = self.anti_vm_custom_lists["knownIps"]
        # user/custom list
        if computer_ip in user_knownIps_list:
            # blacklisted ip
            return True
    # ip not blacklisted
    return False


def vmPathsCheck(self):
    for path in default_vmpaths:
        if os.path.exists(path):
            # vm path found: pc is mote likely one
            return True
    # no vm path found
    return False


def ProcessNamesCheck(self):
    process_names = []
     
    # get all open process names
    for p in psutil.process_iter(attrs=['name']):
        process_names.append(p.info['name'])

    # Check if one process name is in the blacklisted process name list
    for process_name in process_names:
        # check what list to take default or user-specified
        if self.anti_vm_custom_lists["ProcessNames"] is None:
            # default list
            if process_name in default_vmProcesses:
                # blacklisted process open
                return True  
        else:
            user_processNames_list = self.anti_vm_custom_lists["ProcessNames"]
            # user/custom list
            if process_name in user_processNames_list:
                # blacklisted process open
                return True
    # No blacklisted process open
    process_names.clear()
    return False


def ManufactureReleaseCheck(self):
    vm_manufacturer = platform.system()
    vm_release = platform.release()
    
    # Check for common virtualization indicators on Windows
    if "VMware" in vm_manufacturer or "VirtualBox" in vm_manufacturer:
        return True
    
    # Check for common VM release versions
    if "VMWare" in vm_release or "VirtualBox" in vm_release or "QEMU" in vm_release:
        return True
    
    # not Virtualization indicators/ vm release versions detected
    return False