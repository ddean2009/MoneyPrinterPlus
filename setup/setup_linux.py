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

import argparse
import setup_common

errors = 0  # Define the 'errors' variable before using it

# ANSI escape code for yellow color
YELLOW = '\033[93m'
RESET_COLOR = '\033[0m'


def main_menu(platform_requirements_file, show_stdout: bool = False):
    print("Installing python dependencies. This could take a few minutes as it downloads files.")
    print("If this operation ever runs too long, you can rerun this script in verbose mode to check.")

    # Upgrade pip if needed
    setup_common.install('pip', show_stdout=show_stdout)
    setup_common.install_requirements(platform_requirements_file, check_no_verify_flag=False, show_stdout=show_stdout)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--platform-requirements-file', dest='platform_requirements_file', default='requirements_linux.txt', help='Path to the platform-specific requirements file')
    parser.add_argument('--show_stdout', dest='show_stdout', action='store_true', help='Whether to show stdout during installation')
    args = parser.parse_args()

    setup_common.check_python_version()

    setup_common.check_ffmpeg_version()


    main_menu(args.platform_requirements_file, show_stdout=args.show_stdout)
