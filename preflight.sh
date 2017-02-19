# preflight.sh 
# Creator: Luke Donnelly
# Project: LOST	

if [ "$#" -ne 1 ]; then
	echo "Usage: bash preflight.sh <dbname>"
        exit;	
fi


psql $1 -f $HOME/CIS_322/sql/create_tables.sql  #run create_tables script

cp -r $HOME/CIS_322/src/* $HOME/wsgi/           #copy src code to wsgi directory 
