# preflight.sh 
# Creator: Luke Donnelly
# Project: LOST	

if [ "$#" -ne 1 ]; then
	echo "Usage: bash preflight.sh <dbname>"
        exit;	
fi


psql $1 -f  sql/create_tables.sql

cp -r src/* $HOME/wsgi/
