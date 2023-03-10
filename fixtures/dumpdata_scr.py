import subprocess
from config.settings import BASE_DIR


def dumpDataScript():
    working_directory = BASE_DIR

    # command = 'python manage.py dumpdata > data.json'

    command = 'python manage.py dumpdata --exclude admin_interface --exclude contenttypes > fixtures/data.json'

    # Run the command and wait for it to finish
    subprocess.run(command, cwd=working_directory, shell=True)
    subprocess.run(command, shell=True)


if __name__ == '__main__':
    dumpDataScript()
