# preflight.sh 
# Creator: Luke Donnelly
# Assignment 6

if [ "$#" -ne 1 ]; then
	echo "Usage: bash preflight.sh <dbname>"
        exit;	
fi


psql $1 -f $HOME/CIS_322/sql/create_tables.sql

