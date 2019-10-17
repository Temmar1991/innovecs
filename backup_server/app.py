from flask import Flask
from subprocess import Popen, PIPE
import os
import zipfile
import schedule
import time
app = Flask(__name__)
cwd = os.getcwd()

file_name = os.environ.get("DUMP_FILE")


def make_backup(file: str) -> None:
    arg_string = f"mysqldump -h {os.environ.get('HOST')} -u {os.environ.get('DATABASE_USER')} -p {os.environ.get('DATABASE_PASS')} > {file}" + \
                 "_$(date + '%Y-%m-%d %H:%M:%S')"
    arg_list = arg_string.split()
    cmd = Popen(arg_list, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, error = cmd.communicate()
    if cmd.returncode != 0:
        raise RuntimeError(f"Failed to execute command, error {str(error)}")


def archive(zip_name):
    backup_zip = zipfile.ZipFile(os.path.join(cwd, zip_name), 'w')
    for folder, subfolders, files in os.walk(cwd):
        for file in files:
            if file.__contains__('sql'):
                backup_zip.write(os.path.join(folder, file), file, compress_type=zipfile.ZIP_DEFLATED)
    backup_zip.close()


def periodic_beckup():
    schedule.every(5).seconds.do(make_backup(file_name))
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    periodic_beckup()

