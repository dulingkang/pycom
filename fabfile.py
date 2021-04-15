from fabric import Connection, task

USER = 'dulingkang'

ROOT_PATH = '/home/' + USER
TMP_PATH = ROOT_PATH + '/tmp'
COM_PATH = ROOT_PATH + 'app/pycom'

server = Connection('sky', USER)


@task
def deploy():
    print('拉取代码...')
    with server.cd(COM_PATH):
        server.run(f'git pull origin main')
        server.run(f'supervisorctl restart pycom')

