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
