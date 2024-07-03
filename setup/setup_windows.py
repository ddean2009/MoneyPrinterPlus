import setup_common

errors = 0  # Define the 'errors' variable before using it

# ANSI escape code for yellow color
YELLOW = "\033[93m"
RESET_COLOR = "\033[0m"



def install_requirement(headless: bool = False):

    setup_common.install("pip")
    
    setup_common.install_requirements_inbulk(
        "requirements.txt", show_stdout=True, upgrade=False
    )

if __name__ == "__main__":

    setup_common.check_python_version()
    setup_common.check_ffmpeg_version()
    install_requirement()

