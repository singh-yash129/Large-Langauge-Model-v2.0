import os
import subprocess
def run_npx_command(file_name):
    file_path = os.path.join(os.getcwd(), 'tmp', file_name)
    command = f"npx -y prettier@3.4.2 {file_path} | sha256sum"
    return subprocess.getoutput(command)
run_npx_command('README.md')