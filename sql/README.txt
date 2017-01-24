Creator: Luke Donnelly
Project: LOST

The following files are located in the sql directory: 

1. create_tables.sql  -SQL script that creates tables for the LOST database

2. format.py          -python script that formats most of the legacy data so that it may be inserted in the LOST database 
		      -note that some of the data had to be ommitted as it did not fit with our current data model
		      -intake/export dates are not included in this version of the data migration. Date format was inconsistent    througout the legacy data which made it difficult to streamline the process. A later version will incorporate this data
		      -Duplicate product names may appear in the products table. A later version will remove these duplicates

3. import_data 	      -downloads the legacy data files and runs format.py. Must include arguments "database name" "port number" 	  		
