#  Copyright © [2024] 程序那些事
#
#  All rights reserved. This software and associated documentation files (the "Software") are provided for personal and educational use only. Commercial use of the Software is strictly prohibited unless explicit permission is obtained from the author.
#
#  Permission is hereby granted to any person to use, copy, and modify the Software for non-commercial purposes, provided that the following conditions are met:
#
#  1. The original copyright notice and this permission notice must be included in all copies or substantial portions of the Software.
#  2. Modifications, if any, must retain the original copyright information and must not imply that the modified version is an official version of the Software.
#  3. Any distribution of the Software or its modifications must retain the original copyright notice and include this permission notice.
#
#  For commercial use, including but not limited to selling, distributing, or using the Software as part of any commercial product or service, you must obtain explicit authorization from the author.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHOR OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
#  Author: 程序那些事
#  email: flydean@163.com
#  Website: [www.flydean.com](http://www.flydean.com)
#  GitHub: [https://github.com/ddean2009/MoneyPrinterPlus](https://github.com/ddean2009/MoneyPrinterPlus)
#
#  All rights reserved.
#
#

import subprocess
import os
import re
import sys

import pkg_resources

errors = 0  # Define the 'errors' variable before using it

def check_ffmpeg_version():
    try:
        # 尝试执行ffmpeg命令并获取输出
        result = subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        output = result.stdout

        # 检查ffmpeg是否安装
        if result.returncode != 0:
            print("ffmpeg命令不存在或无法执行")
            return False

        # 检查ffmpeg版本号
        for line in output.split('\n'):
            if 'ffmpeg version' in line:
                version = line.split()[2]  # 假设版本号是每行的第2元素
                major_version = int(version.split('.')[0])  # 取出主版本号
                if major_version >= 6:
                    print(f"ffmpeg版本为{version}，满足要求。")
                    return True
                else:
                    print(f"ffmpeg版本为{version}，不满足要求。")
                    return False
        print("无法从输出中找到ffmpeg版本号。")
        return False
    except Exception as e:
        print(f"检查ffmpeg版本时发生错误：{e}")
        return False


def check_python_version():
    """
    Check if the current Python version is within the acceptable range.
    
    Returns:
    bool: True if the current Python version is valid, False otherwise.
    """
    min_version = (3, 10, 0)
    max_version = (3, 13, 0)
    
    try:
        current_version = sys.version_info
        print(f"Python version is {sys.version}")
        
        if not (min_version <= current_version < max_version):
            print(f"The current version of python ({current_version}) is not appropriate to run")
            print("The python version needs to be greater or equal to 3.10 and less than 3.12")
            return False
        return True
    except Exception as e:
        print(f"Failed to verify Python version. Error: {e}")
        return False

def update_submodule(quiet=True):
    """
    Ensure the submodule is initialized and updated.
    
    This function uses the Git command line interface to initialize and update 
    the specified submodule recursively. Errors during the Git operation
    or if Git is not found are caught and logged.
    
    Parameters:
    - quiet: If True, suppresses the output of the Git command.
    """
    git_command = ["git", "submodule", "update", "--init", "--recursive"]
    
    if quiet:
        git_command.append("--quiet")
        
    try:
        # Initialize and update the submodule
        subprocess.run(git_command, check=True)
        print("Submodule initialized and updated.")
        
    except subprocess.CalledProcessError as e:
        # Log the error if the Git operation fails
        print(f"Error during Git operation: {e}")
    except FileNotFoundError as e:
        # Log the error if the file is not found
        print(e)


def clone_or_checkout(repo_url, branch_or_tag, directory_name):
    """
    Clone a repo or checkout a specific branch or tag if the repo already exists.
    For branches, it updates to the latest version before checking out.
    Suppresses detached HEAD advice for tags or specific commits.
    Restores the original working directory after operations.

    Parameters:
    - repo_url: The URL of the Git repository.
    - branch_or_tag: The name of the branch or tag to clone or checkout.
    - directory_name: The name of the directory to clone into or where the repo already exists.
    """
    original_dir = os.getcwd()  # Store the original directory
    try:
        if not os.path.exists(directory_name):
            # Directory does not exist, clone the repo quietly
            
            # Construct the command as a string for logging
            # run_cmd = f"git clone --branch {branch_or_tag} --single-branch --quiet {repo_url} {directory_name}"
            run_cmd = ["git", "clone", "--branch", branch_or_tag, "--single-branch", "--quiet", repo_url, directory_name]


            # Log the command
            print(run_cmd)
            
            # Run the command
            process = subprocess.Popen(
                run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )
            output, error = process.communicate()
            
            if error and not error.startswith("Note: switching to"):
                print(error)
            else:
                print(f"Successfully cloned sd-scripts {branch_or_tag}")
            
        else:
            os.chdir(directory_name)
            subprocess.run(["git", "fetch", "--all", "--quiet"], check=True)
            subprocess.run(["git", "config", "advice.detachedHead", "false"], check=True)
            
            # Get the current branch or commit hash
            current_branch_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode()
            tag_branch_hash = subprocess.check_output(["git", "rev-parse", branch_or_tag]).strip().decode()
            
            if current_branch_hash != tag_branch_hash:
                run_cmd = f"git checkout {branch_or_tag} --quiet"
                # Log the command
                print(run_cmd)
                
                # Execute the checkout command
                process = subprocess.Popen(run_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output, error = process.communicate()
                
                if error:
                    print(error.decode())
                else:
                    print(f"Checked out sd-scripts {branch_or_tag} successfully.")
            else:
                print(f"Current branch of sd-scripts is already at the required release {branch_or_tag}.")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operation: {e}")
    finally:
        os.chdir(original_dir)  # Restore the original directory


def install_requirements_inbulk(requirements_file, show_stdout=True, optional_parm="", upgrade = False):
    if not os.path.exists(requirements_file):
        print(f'Could not find the requirements file in {requirements_file}.')
        return

    print(f'Installing requirements from {requirements_file}...')

    if upgrade:
        optional_parm += " -U"

    if show_stdout:
        run_cmd(f'pip install -r {requirements_file} {optional_parm} -i https://mirrors.aliyun.com/pypi/simple/')
    else:
        run_cmd(f'pip install -r {requirements_file} {optional_parm} -i https://mirrors.aliyun.com/pypi/simple/ --quiet')
    print(f'Requirements from {requirements_file} installed.')
    


# report current version of code
def check_repo_version():
    """
    This function checks the version of the repository by reading the contents of a file named '.release'
    in the current directory. If the file exists, it reads the release version from the file and logs it.
    If the file does not exist, it logs a debug message indicating that the release could not be read.
    """
    if os.path.exists('.release'):
        try:
            with open(os.path.join('./.release'), 'r', encoding='utf8') as file:
                release= file.read()
            
            print(f'version: {release}')
        except Exception as e:
            print(f'Could not read release: {e}')
    else:
        print('Could not read release...')
    
# execute git command
def git(arg: str, folder: str = None, ignore: bool = False):
    """
    Executes a Git command with the specified arguments.

    This function is designed to run Git commands and handle their output.
    It can be used to execute Git commands in a specific folder or the current directory.
    If an error occurs during the Git operation and the 'ignore' flag is not set,
    it logs the error message and the Git output for debugging purposes.

    Parameters:
    - arg: A string containing the Git command arguments.
    - folder: An optional string specifying the folder where the Git command should be executed.
               If not provided, the current directory is used.
    - ignore: A boolean flag indicating whether to ignore errors during the Git operation.
               If set to True, errors will not be logged.

    Note:
    This function was adapted from code written by vladimandic: https://github.com/vladmandic/automatic/commits/master
    """
    
    git_cmd = os.environ.get('GIT', "git")
    result = subprocess.run(f'"{git_cmd}" {arg}', check=False, shell=True, env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=folder or '.')
    txt = result.stdout.decode(encoding="utf8", errors="ignore")
    if len(result.stderr) > 0:
        txt += ('\n' if len(txt) > 0 else '') + result.stderr.decode(encoding="utf8", errors="ignore")
    txt = txt.strip()
    if result.returncode != 0 and not ignore:
        global errors
        errors += 1
        print(f'Error running git: {folder} / {arg}')
        if 'or stash them' in txt:
            print(f'Local changes detected: check log for details...')
        print(f'Git output: {txt}')


def pip(arg: str, ignore: bool = False, quiet: bool = False, show_stdout: bool = False):
    """
    Executes a pip command with the specified arguments.

    This function is designed to run pip commands and handle their output.
    It can be used to install, upgrade, or uninstall packages using pip.
    If an error occurs during the pip operation and the 'ignore' flag is not set,
    it logs the error message and the pip output for debugging purposes.

    Parameters:
    - arg: A string containing the pip command arguments.
    - ignore: A boolean flag indicating whether to ignore errors during the pip operation.
               If set to True, errors will not be logged.
    - quiet: A boolean flag indicating whether to suppress the output of the pip command.
              If set to True, the function will not log any output.
    - show_stdout: A boolean flag indicating whether to display the pip command's output
                    to the console. If set to True, the function will print the output
                    to the console.

    Returns:
    - The output of the pip command as a string, or None if the 'show_stdout' flag is set.
    """
    # arg = arg.replace('>=', '==')
    if not quiet:
        print(f'Installing package: {arg.replace("install", "").replace("--upgrade", "").replace("--no-deps", "").replace("--force", "").replace("  ", " ").strip()}')
    print(f"Running pip: {arg}")
    if show_stdout:
        subprocess.run(f'"{sys.executable}" -m pip {arg}', shell=True, check=False, env=os.environ)
    else:
        result = subprocess.run(f'"{sys.executable}" -m pip {arg}', shell=True, check=False, env=os.environ, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        txt = result.stdout.decode(encoding="utf8", errors="ignore")
        if len(result.stderr) > 0:
            txt += ('\n' if len(txt) > 0 else '') + result.stderr.decode(encoding="utf8", errors="ignore")
        txt = txt.strip()
        if result.returncode != 0 and not ignore:
            global errors # pylint: disable=global-statement
            errors += 1
            print(f'Error running pip: {arg}')
            print(f'Pip output: {txt}')
        return txt

def installed(package, friendly: str = None):
    """
    Checks if the specified package(s) are installed with the correct version.
    This function can handle package specifications with or without version constraints,
    and can also filter out command-line options and URLs when a 'friendly' string is provided.
    
    Parameters:
    - package: A string that specifies one or more packages with optional version constraints.
    - friendly: An optional string used to provide a cleaner version of the package string
                that excludes command-line options and URLs.

    Returns:
    - True if all specified packages are installed with the correct versions, False otherwise.
    
    Note:
    This function was adapted from code written by vladimandic.
    """
    
    # Remove any optional features specified in brackets (e.g., "package[option]==version" becomes "package==version")
    package = re.sub(r'\[.*?\]', '', package)

    try:
        if friendly:
            # If a 'friendly' version of the package string is provided, split it into components
            pkgs = friendly.split()
            
            # Filter out command-line options and URLs from the package specification
            pkgs = [
                p
                for p in package.split()
                if not p.startswith('--') and "://" not in p
            ]
        else:
            # Split the package string into components, excluding '-' and '=' prefixed items
            pkgs = [
                p
                for p in package.split()
                if not p.startswith('-') and not p.startswith('=')
            ]
            # For each package component, extract the package name, excluding any URLs
            pkgs = [
                p.split('/')[-1] for p in pkgs
            ]

        for pkg in pkgs:
            # Parse the package name and version based on the version specifier used
            if '>=' in pkg:
                pkg_name, pkg_version = [x.strip() for x in pkg.split('>=')]
            elif '==' in pkg:
                pkg_name, pkg_version = [x.strip() for x in pkg.split('==')]
            else:
                pkg_name, pkg_version = pkg.strip(), None

            # Attempt to find the installed package by its name
            spec = pkg_resources.working_set.by_key.get(pkg_name, None)
            if spec is None:
                # Try again with lowercase name
                spec = pkg_resources.working_set.by_key.get(pkg_name.lower(), None)
            if spec is None:
                # Try replacing underscores with dashes
                spec = pkg_resources.working_set.by_key.get(pkg_name.replace('_', '-'), None)

            if spec is not None:
                # Package is found, check version
                version = pkg_resources.get_distribution(pkg_name).version
                print(f'Package version found: {pkg_name} {version}')

                if pkg_version is not None:
                    # Verify if the installed version meets the specified constraints
                    if '>=' in pkg:
                        ok = version >= pkg_version
                    else:
                        ok = version == pkg_version

                    if not ok:
                        # Version mismatch, log warning and return False
                        print(f'Package wrong version: {pkg_name} {version} required {pkg_version}')
                        return False
            else:
                # Package not found, log debug message and return False
                print(f'Package version not found: {pkg_name}')
                return False

        # All specified packages are installed with the correct versions
        return True
    except ModuleNotFoundError:
        # One or more packages are not installed, log debug message and return False
        print(f'Package not installed: {pkgs}')
        return False



# install package using pip if not already installed
def install(
    package,
    friendly: str = None,
    ignore: bool = False,
    reinstall: bool = False,
    show_stdout: bool = False,
):
    """
    Installs or upgrades a Python package using pip, with options to ignode errors,
    reinstall packages, and display outputs.
    
    Parameters:
    - package (str): The name of the package to be installed or upgraded. Can include
      version specifiers. Anything after a '#' in the package name will be ignored.
    - friendly (str, optional): A more user-friendly name for the package, used for
      logging or user interface purposes. Defaults to None.
    - ignore (bool, optional): If True, any errors encountered during the installation
      will be ignored. Defaults to False.
    - reinstall (bool, optional): If True, forces the reinstallation of the package
      even if it's already installed. This also disables any quick install checks. Defaults to False.
    - show_stdout (bool, optional): If True, displays the standard output from the pip
      command to the console. Useful for debugging. Defaults to False.

    Returns:
    None. The function performs operations that affect the environment but does not return
    any value.
    
    Note:
    If `reinstall` is True, it disables any mechanism that allows for skipping installations
    when the package is already present, forcing a fresh install.
    """
    # Remove anything after '#' in the package variable
    package = package.split('#')[0].strip()

    if reinstall:
        global quick_allowed   # pylint: disable=global-statement
        quick_allowed = False
    if reinstall or not installed(package, friendly):
        pip(f'install --upgrade {package} -i https://mirrors.aliyun.com/pypi/simple/', ignore=ignore, show_stdout=show_stdout)


def process_requirements_line(line, show_stdout: bool = False):
    # Remove brackets and their contents from the line using regular expressions
    # e.g., diffusers[torch]==0.10.2 becomes diffusers==0.10.2
    package_name = re.sub(r'\[.*?\]', '', line)
    install(line, package_name, show_stdout=show_stdout)


def install_requirements(requirements_file, check_no_verify_flag=False, show_stdout: bool = False):
    if check_no_verify_flag:
        print(f'Verifying modules installation status from {requirements_file}...')
    else:
        print(f'Installing modules from {requirements_file}...')
    with open(requirements_file, 'r', encoding='utf8') as f:
        # Read lines from the requirements file, strip whitespace, and filter out empty lines, comments, and lines starting with '.'
        if check_no_verify_flag:
            lines = [
                line.strip()
                for line in f.readlines()
                if line.strip() != ''
                and not line.startswith('#')
                and line is not None
                and 'no_verify' not in line
            ]
        else:
            lines = [
                line.strip()
                for line in f.readlines()
                if line.strip() != ''
                and not line.startswith('#')
                and line is not None
            ]

        # Iterate over each line and install the requirements
        for line in lines:
            # Check if the line starts with '-r' to include another requirements file
            if line.startswith('-r'):
                # Get the path to the included requirements file
                included_file = line[2:].strip()
                # Expand the included requirements file recursively
                install_requirements(included_file, check_no_verify_flag=check_no_verify_flag, show_stdout=show_stdout)
            else:
                process_requirements_line(line, show_stdout=show_stdout)


def ensure_base_requirements():
    try:
        import rich   # pylint: disable=unused-import
    except ImportError:
        install('--upgrade rich', 'rich')
        
    try:
        import packaging
    except ImportError:
        install('packaging')


def run_cmd(run_cmd):
    try:
        subprocess.run(run_cmd, shell=True, check=False, env=os.environ)
    except subprocess.CalledProcessError as e:
        print(f'Error occurred while running command: {run_cmd}')
        print(f'Error: {e}')


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def write_to_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
    except IOError as e:
        print(f'Error occurred while writing to file: {file_path}')
        print(f'Error: {e}')


def clear_screen():
    # Check the current operating system to execute the correct clear screen command
    if os.name == 'nt':  # If the operating system is Windows
        os.system('cls')
    else:  # If the operating system is Linux or Mac
        os.system('clear')

