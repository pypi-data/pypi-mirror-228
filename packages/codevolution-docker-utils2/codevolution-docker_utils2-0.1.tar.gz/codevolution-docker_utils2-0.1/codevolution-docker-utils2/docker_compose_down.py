from library import Docker


if __name__ == '__main__':
    docker = Docker('../', True)
    print('1/2. Starting compose down...')
    result = docker.compose_down()

    if result[0]:
        print(f'2/2. Compose stopped properly.')
    else:
        print(f'2/2. Compose stopped with error: {result[1]}.')
