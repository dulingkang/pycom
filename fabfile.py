from fabric import Connection, task

USER = 'dulingkang'

ROOT_PATH = '/home/' + USER
TMP_PATH = ROOT_PATH + '/tmp'
COM_PATH = ROOT_PATH + '/app/pycom'

server = Connection('47.111.166.10', USER)


@task
def deploy(context):
    print('开始部署...')
    with server.cd(COM_PATH):
        server.run(f'git pull origin main')
        server.run(f'sudo supervisorctl restart pycom')
    print('部署完成...')

