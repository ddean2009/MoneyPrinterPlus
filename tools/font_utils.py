import subprocess
import re


# fc-scan Songti.ttc | grep fullname

def get_font_fullname(font_path):
    try:
        # Run fc-scan and capture the output
        result = subprocess.run(['fc-scan', font_path], capture_output=True, text=True)

        # Check for errors
        if result.returncode != 0:
            print(result.stderr)
            return None

        # Use regex to find the fullname
        match = re.search(r'fullname: "(.*?)"', result.stdout)

        if match:
            return match.group(1)  # Return the extracted font name
        else:
            print("Font name not found in fc-scan output")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None
