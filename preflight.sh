#Shell scrript to install tables and transfer files to the LOST WSGI

psql $1 -f ./sql/create_tables.sql 
psql $1 -f ./sql/inserts.sql

cp -r $HOME/CIS_322/src/* $HOME/wsgi/
