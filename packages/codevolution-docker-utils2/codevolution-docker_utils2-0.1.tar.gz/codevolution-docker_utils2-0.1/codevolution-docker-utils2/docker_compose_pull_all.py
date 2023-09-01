from library import Docker


if __name__ == '__main__':
    docker = Docker('../', False)
    services = docker.compose_get_services()

    print(f'Pulling {len(services)} services...')

    for service in services:
        print(f'- {service}')
        result = docker.compose_pull(service)

        if result[0]:
            print(f'  - Pulled')
        else:
            if result[1]:
                print(f'  - Error: {result[1]}')
            else:
                print(f'  - Already up to date')
