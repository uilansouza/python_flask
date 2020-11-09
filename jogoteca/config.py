import os
SECRET_KEY = "alura"
MYSQL_HOST = '0.0.0.0'
MYSQL_USER = 'admin'
MYSQL_PASSWORD = '39411434'
MYSQL_DB = 'jogoteca'
MSQL_PORT = 3306
#root_path
# dirname = nome do diretório... aspath = pega o nome do caminho abosluto em relação ao arquivo atual(jogoteca)
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__))\
              + '/uploads'
