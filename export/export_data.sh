if [ -d "$2" ]
then
	rm -r $2
	mkdir $2
else
	mkdir $2
fi

python3  users.py $1 > $2/users.csv
python3  facilities.py $1 > $2/facilities.csv
python3  assets.py $1 > $2/assets.csv
python3  transfers.py $1 > $2/transfers.csv
