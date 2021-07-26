import urllib.request
import subprocess
import shutil
import os
import tkinter
from tkinter import filedialog
from pathlib import Path
from messages import TerminalMessageHandler
import xml.etree.ElementTree as et


PROGRAM_VERSION = "1.0.0"
TERMINAL_COLS = 85
MESSAGE_HANDLER = TerminalMessageHandler(TERMINAL_COLS)


def get_github_version(github_url):
    """
    Get the program version number that is on GitHub. This must be a specific format starting with 'VERSION-'
    :param github_url: URL for GitHub RAW link.
    :return: Everything after 'VERSION-' or Null if not found.
    """
    update_source = urllib.request.urlopen(github_url)
    contents = update_source.readlines()
    update_source.close()

    for line in contents:
        line = str(line).strip("b'")
        line = line.strip('\\n')
        if line.startswith("VERSION-"):
            line = line.strip("VERSION-")
            return line
    return None


def version_check(github_url=None):
    """
    Check current program version against the one that is hosted on GitHub. Prompt user if versions are different.
    :param github_url: URL for GitHub RAW link.
    :return: Nothing
    """
    print(MESSAGE_HANDLER.update_msg())

    # TODO - Add auto updater?
    github_version = get_github_version(github_url)

    if PROGRAM_VERSION == github_version:
        return
    else:
        while True:
            continue_var = input(MESSAGE_HANDLER.update_msg(update_available=True, prog_version=PROGRAM_VERSION,
                                                            gh_version=github_version)).lower().strip()
            if continue_var == "y":
                return
            elif continue_var == "n":
                exit()
            else:
                print(f"'\n{continue_var}' is not a valid entry.\n\n")


def process_exists(process_name="vERAM.exe"):
    """
    Check to see if a process is running
    :param process_name: full name of process (Str) (i.g vERAM.exe)
    :return: boolean
    """
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    output = subprocess.check_output(call).decode()
    last_line = output.strip().split('\r\n')[-1]
    return last_line.lower().startswith(process_name.lower())


def select_file(file_types,
                title="Select your vERAMConfig.xml",
                initial_dir=Path(os.path.join(os.environ['USERPROFILE'], "AppData", "Local")), veram=True):
    """
    File selection dialog pop-up box.
    :param file_types: filtered file types to display (i.e. [("vERAMConfig", ".xml")] )
    :param title: dialog selection pop-up box title
    :param initial_dir: directory path the pop-up should start in.
    :return: selected file full file path
    """
    print(MESSAGE_HANDLER.select_file_msg(veram))
    root = tkinter.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(title=title,
                                           initialdir=initial_dir,
                                           filetypes=file_types)
    if len(file_path) > 1:
        return file_path
    else:
        input(MESSAGE_HANDLER.warning_msg(select_file=True))
        exit()


def make_backup(file_path):
    """
    Create Backup file for vERAMConfig.xml on the user's Desktop
    :param file_path: must be full file path to vERAMConfig.xml file.
    :return: nothing
    """
    v_config_file = Path(file_path)
    if v_config_file.exists():
        src_file_name = str(file_path).split("\\")[-1]
        backup_file_path = os.path.join(os.environ['USERPROFILE'], 'Desktop', f'BACKUP-{src_file_name}')
        if Path(backup_file_path).exists():
            overwrite = input(MESSAGE_HANDLER.warning_msg(backup_overwrite=True)).lower().strip()
            if overwrite == "y":
                shutil.copy2(v_config_file, backup_file_path)
            else:
                exit()
        else:
            shutil.copy2(v_config_file, backup_file_path)
    else:
        while True:
            new_file_path = Path(select_file([("vERAMConfig", ".xml")]))
            if str(new_file_path).split('\\')[-1] == "vERAMConfig.xml":
                break
        make_backup(new_file_path)


def read_from_file():
    """
    Read user created custom WX and ALT .txt file
    :return: dictionary with required info (ID, WX's, ALT's)
    """
    info = {}
    filepath = select_file([("Custom .txt", ".txt")],
                           title="Select TXT file with Wx Stations and Altimeter settings",
                           initial_dir=Path(os.path.join(os.environ['USERPROFILE'], "Downloads")), veram=False)
    with open(filepath, "r") as file:
        for line in file.readlines():
            if line.upper().startswith("ARTCC:"):
                info['ID'] = line.upper().strip().replace('ARTCC:', '')
            elif line.upper().startswith('ALT:'):
                info['ALT'] = line.upper().replace('ALT:', '').split(' ')
            elif line.upper().startswith('WX:'):
                info['WX'] = line.upper().replace('WX:', '').split(' ')
            else:
                continue
    keys = info.keys()
    if 'ID' in keys and 'WX' in keys and 'ALT' in keys:
        if input(MESSAGE_HANDLER.get_alt_data_input_msg("VERIFY", info)).strip().upper() == "Y":
            return info
        else:
            # TODO - Notify user why program is exiting?
            exit()
    else:
        input(MESSAGE_HANDLER.warning_msg(cd_invalid_file=True))
        exit()


def get_alt_wx_input():
    info = dict()
    while True:
        info['ID'] = input(MESSAGE_HANDLER.get_alt_data_input_msg("ARTCC")).upper().strip()
        info['WX'] = input(MESSAGE_HANDLER.get_alt_data_input_msg("WX")).upper().strip().split(' ')
        info['ALT'] = input(MESSAGE_HANDLER.get_alt_data_input_msg("ALT")).upper().strip().split(' ')
        verified = input(MESSAGE_HANDLER.get_alt_data_input_msg("VERIFY", info)).upper().strip()
        if verified == "Y":
            break
        else:
            info = {}
    return info


def default_zlc():
    info = {'ID': 'ZLC',
            'ALT': ["KBIL", "KBKE", "KBOI", "KBPI", "KBTM", "KBZN", "KCDC", "KCOD", "KCTB", "KEKO", "KELY",
                    "KGDV", "KGGW", "KGJT", "KGPI", "KGTF", "KHLN", "KHVR", "KIDA", "KJAC", "KLWT", "KMLS",
                    "KMSO", "KMUO", "KOGD", "KPIH", "KPVU", "KRIW", "KRKS", "KSDY", "KSHR", "KSLC", "KSUN",
                    "KTPH", "KTWF", "KVEL", "KWMC", "KWRL", "KXWA"],
            'WX': ["KBIL", "KBOI", "KBZN", "KGPI", "KGTF", "KHLN", "KIDA", "KJAC", "KMSO", "KOGD", "KPIH",
                   "KPVU", "KSLC", "KSUN", "KTWF"]}
    verified = input(MESSAGE_HANDLER.get_alt_data_input_msg("VERIFY", info)).upper().strip()
    if verified == "Y":
        return info
    else:
        # TODO - Tell user why program exits?
        exit()


def user_menu_option_custom_data(prev_choice=None):
    available_choices = ['R', 'M', 'D', 'X']

    while True:
        if prev_choice is not None:
            if len(prev_choice) > MESSAGE_HANDLER.max_cols - len('WARNING - INVALID SELECTION ') - 4:
                prev_choice = prev_choice[:MESSAGE_HANDLER.max_cols - len('WARNING - INVALID SELECTION ') - 4]
            user_choice = input(MESSAGE_HANDLER.warning_msg(cd_invalid_choice=True,
                                                            additional_data=prev_choice)).upper().strip()
        else:
            user_choice = input(MESSAGE_HANDLER.custom_data_msg()).upper().strip()

        if user_choice in available_choices:
            if user_choice == "R":
                info_dict = read_from_file()
                return info_dict
            elif user_choice == "M":
                info_dict = get_alt_wx_input()
                return info_dict
            elif user_choice == "D":
                info_dict = default_zlc()
                return info_dict
            elif user_choice == "X":
                exit()
        else:
            prev_choice = user_choice.upper().strip()


def process_xml_config(src_file_path):
    """
    Process and add standard Altimeters and Weather Reports to current vERAM config file.
    :param src_file_path: full file path to vERAMConfig.xml
    :return: nothing
    """
    data = user_menu_option_custom_data()

    print(MESSAGE_HANDLER.processing_msg())
    tree = et.parse(src_file_path)
    root = tree.getroot()
    facilities = root.find('Facilities')
    eram_facilities = facilities.findall('ERAMFacility')

    for eram_facility in eram_facilities:
        if eram_facility.find('ID').text == data['ID']:
            local = eram_facility.find('Local')
            alt = local.find('RequestedAltimeters')
            wx = local.find('RequestedWeatherReports')

            for child in list(alt):
                alt.remove(child)
            for child in list(wx):
                wx.remove(child)

            for altimeter in data['ALT']:
                new_tag = et.SubElement(alt, 'string')
                new_tag.text = altimeter
            for weather_report in data['WX']:
                new_tag = et.SubElement(wx, 'string')
                new_tag.text = weather_report

    tree.write(src_file_path)


def main():
    """
    Main Entry Point for Program
    :return: nothing
    """
    config_file_path = Path(os.path.join(os.environ['USERPROFILE'], "AppData", "Local", "vERAM", "vERAMConfig.xml"))
    github_url = "https://raw.githubusercontent.com/KSanders7070/ZLC_vERAM_Wx_Setup/main/Version_Check"

    input(MESSAGE_HANDLER.about_msg())

    version_check(github_url)

    if process_exists():
        print(MESSAGE_HANDLER.warning_msg(process_exists=True))
        input(" Press <ENTER> to close.")
        exit()

    make_backup(config_file_path)

    process_xml_config(config_file_path)

    input(MESSAGE_HANDLER.complete_msg())
    

if __name__ == '__main__':
    os.system(f'mode con: cols={TERMINAL_COLS} lines=25')
    os.system('title ZLC vERAM WX Setup')
    main()
