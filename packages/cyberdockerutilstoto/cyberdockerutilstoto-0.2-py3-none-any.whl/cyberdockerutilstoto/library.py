import os
import time
import subprocess
import yaml


class Docker:
    def __init__(self, project_directory:str, debug:bool=False):
        self.project_directory = project_directory
        self.branch_name = self.get_git_branchname()
        self.bucket_name = self.get_directory_name()
        self.project_name  = f'{self.bucket_name}_{self.branch_name}'
        self.debug = debug

    def __run(self, *args):
        subprocess_args = ('docker',)
        subprocess_args += args
        subprocess_command = ' ' . join(subprocess_args)

        if self.debug:
            print(f'  Debug: {subprocess_command}')

        return subprocess.run(subprocess_args, capture_output=True, text=True)

    def compose_get_services(self):
        file_path = os.path.join(self.project_directory, 'docker-compose.yml')

        with open(file_path, 'r') as file:
            docker_compose_data = yaml.safe_load(file)
            return list(docker_compose_data['services'].keys())

    def get_git_branchname(self):
        return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()

    def get_directory_name(self):
        project_directory_absolute = os.path.normpath(os.path.join(os.getcwd(), self.project_directory))
        return os.path.basename(project_directory_absolute)

    def compose_pull(self, service_name):
        result = self.__run('compose', '--project-directory', self.project_directory, 'pull', service_name)

        if result.returncode != 0:
            return (False, result.stderr)
        else:
            if result.stderr.find('Downloading') > 0 or result.stderr.find('Extracting') > 0:
                return (True, None)
            else:
                return (False, None)

    def compose_up(self):
        result = self.__run('compose', '--project-directory', self.project_directory, '-p', self.project_name, 'up', '--detach')

        if result.returncode == 0:
            return (True, None)
        else:
            return (False, result.stderr)

    def compose_down(self):
        result = self.__run('compose', '--project-directory', self.project_directory, '-p', self.project_name, 'down')

        if result.returncode != 0:
            return (False, result.stderr)
        else:
            if result.stderr.find('Started') > 0:
                return (True, None)
            else:
                return (False, result.stderr)

    def compose_is_up(self):
        output = self.__run('ps')

        if output.stdout.find(self.project_name) > 0:
            return True
        else:
            return False

    def compose_sleep_while_is_not_started(self, max_attempts=10, sleep_seconds=10):
        current_attempts = 0

        while True:
            time.sleep(sleep_seconds)
            current_attempts += 1

            if current_attempts > max_attempts:
                return False

            if self.compose_is_up():
                return True

    def compose_restart(self):
        if self.compose_is_up():
            self.compose_down()

        return self.compose_up()

    def compose_exec(self, service_name, command):
        container_name = f'{self.project_name}-{service_name}-1'
        return self.container_exec(container_name, command)

    def container_exec(self, container_name, command):
        commands = command.split(' ')
        return self.__run('exec', '-it', container_name, *commands)
