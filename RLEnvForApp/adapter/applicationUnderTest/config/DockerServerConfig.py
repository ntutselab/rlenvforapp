MAXIMUM_WAITING_TIMEOUT = 1000
DOCKER_IMAGE_CREATOR = "ntutselab"
APPLICATION_NAME = "Application"
PORT = "3000"


def docker_compose_file_name(applicationName: str, port: str):
    fileName = f"docker_compose_{applicationName}_{port}.yml"
    return fileName


def docker_compose_file_content(dockerImageCreator: str = DOCKER_IMAGE_CREATOR, applicationName: str = APPLICATION_NAME,
                             port: str = PORT):
    if applicationName == "timeoff_management_with_coverage":
        return get_timeoff_docker_compose_file(port)

    if applicationName == "keystonejs_with_coverage":
        return get_keystone_js_docker_compose_file(port)

    if applicationName == "nodebb_with_coverage":
        return get_nodebb_docker_compose_file(port)

    if applicationName == "django_blog_with_no_coverage":
        return get_django_blog_docker_compose_file(port)

    if applicationName == "spring_petclinic_with_no_coverage":
        return get_spring_petclinic_docker_compose_file(port)

    if applicationName == "kimai":
        return get_kimai_docker_compose_file(port)

    if applicationName == "astuto":
        return get_astuto_docker_compose_file(port)

    if applicationName == "oscar":
        return get_oscar_docker_compose_file(port)

    if applicationName == "svelte_commerce":
        return get_svelte_commerce_docker_compose_file(port)

    # compose_file_content = '{applicationName}_{port}:\n' \
    #                        ' image: {dockerImageCreator}/{applicationName}\n' \
    #                        ' ports:\n' \
    #                        '  - "{port}:3000"'
    #
    # if applicationName == "nodebb_with_coverage":
    #     compose_file_content = '{applicationName}_{port}:\n' \
    #                            ' image: {dockerImageCreator}/{applicationName}\n' \
    #                            ' ports:\n' \
    #                            '  - "{port}:4567"\n' \
    #                            ' links:\n' \
    #                            '  - mongodb_{port}\n' \
    #                            ' environment:\n' \
    #                            '  - MONGO_HOST=mongodb_{port}\n' \
    #                            'mongodb_{port}:\n' \
    #                            ' image: ntutselab/mongo'
    #
    # if applicationName == "keystonejs_with_coverage":
    #     dbPort = 27000 + int(port) % 3000
    #     compose_file_content = '{applicationName}_{port}:\n' \
    #                            ' image: {dockerImageCreator}/{applicationName}\n' \
    #                            ' ports:\n' \
    #                            '  - "{port}:3000"\n' \
    #                            ' links:\n' \
    #                            '  - nameOfMongoDB\n' \
    #                            ' environment:\n' \
    #                            '  - MONGO_URI=mongodb://nameOfMongoDB:27017/\n' \
    #                            'nameOfMongoDB:\n' \
    #                            ' image: mongo\n' \
    #                            ' ports:\n' \
    #                            '  - "' + str(dbPort) + ':27017"'
    #
    # if applicationName == "wagtails_with_coverage":
    #     dockerImageCreator = "ntuthongkaihuang"
    #     applicationName = "wagtail"
    #     compose_file_content = '{applicationName}_{port}:\n' \
    #                            ' image: {dockerImageCreator}/{applicationName}\n' \
    #                            ' ports:\n' \
    #                            '  - "{port}:8000"'
    #
    # if applicationName == "django_blog_with_no_coverage":
    #     dockerImageCreator = "lidek213"
    #     applicationName = "django-blog_for_experiment"
    #     compose_file_content = '{applicationName}_{port}:\n' \
    #                            ' image: {dockerImageCreator}/{applicationName}\n' \
    #                            ' ports:\n' \
    #                            '  - "{port}:3000"'
    # if applicationName == "spring_petclinic_with_no_coverage":
    #     dockerImageCreator = "lidek213"
    #     applicationName = "spring-petclinic_for_experiment"
    #     compose_file_content = '{applicationName}_{port}:\n' \
    #                            ' image: {dockerImageCreator}/{applicationName}\n' \
    #                            ' command: java -jar /spring-petclinic/build/libs/spring-petclinic-2.6.0.jar /spring-petclinic/build/libs/spring-petclinic-2.6.0-plain.jar\n' \
    #                            ' ports:\n' \
    #                            '  - "{port}:8080"'
    #
    # compose_file_content = compose_file_content.format(dockerImageCreator=dockerImageCreator,
    #                                                    applicationName=applicationName, port=port)
    # return compose_file_content


def create_docker_compose_command(dockerComposePath: str):
    return ["docker-compose", "-f", dockerComposePath, "up", "-d"]


def remove_docker_compose_command(dockerComposePath: str):
    return ["docker-compose", "-f", dockerComposePath, "rm", "-svf"]


def find_docker_compose_container_id_command(dockerComposePath: str):
    return ["docker-compose", "-f", dockerComposePath, "ps", "-q"]


def get_timeoff_docker_compose_file(port: str = PORT):
    config = f'''
    services:
      timeoff_management_with_coverage_{port}:
        image: ntutselab/timeoff_management_with_coverage
        ports:
        - "127.0.0.1:{port}:3000"
    '''
    return config


def get_keystone_js_docker_compose_file(port: str = PORT):
    config = f'''
    services:
      keystonejs_with_coverage_{port}:
        image: ntutselab/keystonejs_with_coverage
        ports:
          - '{port}:3000'
        links:
          - nameOfMongoDB
        environment:
          - 'MONGO_URI=mongodb://nameOfMongoDB:27017/'
      nameOfMongoDB:
        image: ntutselab/mongo
        ports:
          - '27001:27017'
    '''
    return config


def get_nodebb_docker_compose_file(port: str = PORT):
    config = f'''
    services:
      nodebb_with_coverage_{port}:
        image: ntutselab/nodebb_with_coverage
        ports:
          - '{port}:4567'
        links:
          - mongodb_1
        environment:
          - MONGO_HOST=mongodb_1
      mongodb_1:
        image: ntutselab/mongo
    '''
    return config


def get_django_blog_docker_compose_file(port: str = PORT):
    config = f'''
    services:
      django_blog_with_no_coverage_{port}:
        image: lidek213/django-blog_for_experiment
        ports:
          - "127.0.0.1:{port}:3000"
    '''
    return config


def get_spring_petclinic_docker_compose_file(port: str = PORT):
    config = f'''
    services:
      spring_petclinic_with_no_coverage_{port}:
        image: lidek213/spring-petclinic_for_experiment:latest
        command: java -jar /spring-petclinic/build/libs/spring-petclinic-2.6.0.jar /spring-petclinic/build/libs/spring-petclinic-2.6.0-plain.jar
        ports:
          - '{port}:8080'
    '''
    return config


def get_kimai_docker_compose_file(port: str = PORT):
    config = f'''
    version: '3.5'
    services:

      sqldb:
        image: mysql:5.7
        volumes:
          - kimai-mysql:/var/lib/mysql
        environment:
          - MYSQL_DATABASE=kimai
          - MYSQL_USER=kimaiuser
          - MYSQL_PASSWORD=kimaipassword
          - MYSQL_ROOT_PASSWORD=changemeplease
        command: --default-storage-engine innodb
        restart: unless-stopped
        healthcheck:
          test: mysqladmin -p$$MYSQL_ROOT_PASSWORD ping -h localhost
          interval: 20s
          start_period: 10s
          timeout: 10s
          retries: 3

      kimai_{port}:
        image: kimai/kimai2:apache
        volumes:
          - kimai-var:/opt/kimai/var
        ports:
          - {port}:8001
        environment:
          - ADMINMAIL=vector@selab.com
          - ADMINPASS=selab1623
          - DATABASE_URL=mysql://kimaiuser:kimaipassword@sqldb/kimai
          - TRUSTED_HOSTS=nginx,localhost,127.0.0.1
        restart: unless-stopped

    volumes:
      kimai-var:
      kimai-mysql:
    '''
    return config


def get_astuto_docker_compose_file(port: str = PORT):
    config = f'''
    version: '3.4'
    services:
      db:
        image: postgres:14.5
        environment:
          POSTGRES_USER: astuto
          POSTGRES_PASSWORD: dbpass
      astuto_{port}:
        image: riggraz/astuto
        environment:
          POSTGRES_USER: astuto
          POSTGRES_PASSWORD: dbpass
          BASE_URL: http://localhost:3000
          SECRET_KEY_BASE: secretkeybasehere
        ports:
          - "{port}:3000"
        depends_on:
          - db
    '''
    return config


def get_oscar_docker_compose_file(port: str = PORT):
    config = f'''
    services:
      oscar:
        image: oscarcommerce/django-oscar-sandbox
        ports:
          - "{port}:8080"
    '''
    return config


def get_svelte_commerce_docker_compose_file(port: str = PORT):
    config = f'''
    version: '3.8'
    services:
      svelte-commerce:
        image: ghcr.io/itswadesh/svelte-commerce
        ports:
          - "{port}:3000"
    '''
    return config
