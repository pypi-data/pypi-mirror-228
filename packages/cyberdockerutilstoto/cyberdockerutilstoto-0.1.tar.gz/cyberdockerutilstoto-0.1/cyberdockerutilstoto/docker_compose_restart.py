from library import Docker


if __name__ == '__main__':
    docker = Docker('../', True)
    service_name = 'app_gunicorn'
    print(f'1/6. Restarting docker compose...')

    result = docker.compose_restart()

    if result[0]:
        print(f'2/6. Restart.')
        print(f'3/6. Waiting complete restart...')
        docker.compose_sleep_while_is_not_started()
        print(f'4/6. Restarted.')
        command = 'python3 manage.py migrate'
        print(f'5/6. Executing {command} on {service_name}...')
        output = docker.compose_exec(service_name, command)
        print(f'6/6. {service_name} command output: {output}')
    else:
        print(f'2/6. Error: {result[1]}')
