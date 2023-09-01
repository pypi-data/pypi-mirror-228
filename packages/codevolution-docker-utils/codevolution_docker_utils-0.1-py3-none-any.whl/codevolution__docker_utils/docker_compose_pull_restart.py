from library import Docker


if __name__ == '__main__':
    docker = Docker('../', True)
    service_name = 'app_gunicorn'
    print(f'1/6. Pulling {service_name}...')
    result = docker.compose_pull(service_name)

    if result[0]:
        print(f'2/6. Pulled properly.')
        print(f'3/6. Restating docker compose...')

        result = docker.compose_restart()

        if result[0]:
            print(f'4/6. Restarted.')
            command = 'python3 manage.py migrate'
            print(f'5/6. Executing {command} on {service_name}...')
            output = docker.compose_exec(service_name, command)
            print(f'6/6. {service_name} command output: {output.stderr}')
        else:
            print(f'6/6. Error: {result[1]}')
    else:
        if result[1]:
            print(f'2/6. Pull error: {result[1]}.')
        else:
            print(f'2/6. {service_name} has the latest version.')
