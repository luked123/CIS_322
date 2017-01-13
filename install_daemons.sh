#This is a basic shell script which will install and configure
#postgres 9.5.5 and Apache httpd-2.4.25 with the path specified by argument 1

#postgres installation
git clone https://github.com/postgres/postgres
cd postgres
git checkout remotes/origin/REL9_5_STABLE
./configure --prefix=$1
make 
make install 
cd .. 

#Apache httpd instalation 
curl http://www-us.apache.org/dist//httpd/httpd-2.4.25.tar.gz | tar xvz
cd httpd-2.4.25
./configure --prefix=$1 --with-port=8080 #changes default port
make 
make install
cd .. 
