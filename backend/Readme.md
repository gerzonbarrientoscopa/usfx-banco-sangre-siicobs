create seed
python manage.py dumpdata > seed.json

load seed
python manage.py loaddata seed.json

git config user.name "Pamela B"
git config user.email pamelitabbpamelitabb@gmail.com

docker sql server
docker pull mcr.microsoft.com/azure-sql-edge

docker run -d --name MySQLServer -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=B4nc0Sangr3' -p 1433:1433 mcr.microsoft.com/azure-sql-edge

# install 
sqlserver
pip install mssql-django
{
'ENGINE': 'mssql'
}
brew install unixodbc
export LDFLAGS="-L/opt/homebrew/Cellar/unixodbc/2.3.11/lib"
export CPPFLAGS="-I/opt/homebrew/Cellar/unixodbc/2.3.11/include"
pip install pyodbc

pip install --no-binary :all: pyodbc
## install sql server ubuntu
https://learn.microsoft.com/es-es/sql/linux/quickstart-install-connect-ubuntu?view=sql-server-linux-ver16&preserve-view=true
https://learn.microsoft.com/th-th/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-2016&tabs=alpine18-install%2Cubuntu17-install%2Cdebian8-install%2Credhat7-13-install%2Crhel7-offline#17
login docker
sudo docker exec -it MySQLServer "bash"
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P "B4nc0Sangr3"

## import donors from donors.json
1. copy donors.json file to donors/fixtures/donors.json
2. python manage.py load_initial_data