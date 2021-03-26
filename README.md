''' Project for representing covid dataset in knowledge graphs using grapgDB'''

Inside ontology folder, we have two sub-folder (screenshots and graph) and two files (one python file with name read_covid_dataset and turtle file with name covid).

Steps to follow:

1. Run read_covid_dataset python file to read csv covid data and store the data locally, please remember to change the path inside the file to store it locally. Also install pandas by running pip install pandas on command line.

2. Inside graph sub-folder:

- we have Dockerfile which is used to run free version of GraphDB.

- Then, we have GraphDB zip file which is very important to run the current free version of GraphDB (9.6.0).

- And, we have graphdb tar file with name graphdb which can be directly used in docker to run the docker image that I have     created and to visualize data which I have worked with. You can see the data which is present in my GraphDB repository and the name of my repository is rohit. (you can remove this tar file if you creating your new docker image and for that just use Dockerfile and graphdb.zip file inside graph folder)

3. If you are running your own image then just make graph folder on your desktop with Dockerfile and graphdb zip file in it without using tar file and build the image using:

    - docker build -t imagename:tag . 
    - docker run --publish 7200:7200 imagename



once the graphdb is up, you can import rdf data by using covid.ttl file which is present here. One important thing covid.ttl includes rdf reprentation for 15 countries that I have created from csv covid data (see read_covid_dataset python file).

4. Finally, there is another folder named screenshots, where you can see some of the queries that I ran and their results. Also, there is some other screenshots depicting some of the insights of the work (different classes, their relationship and so on).

''' steps I have used to create image,container and to save it into tar file'''

docker build -t grapgdb:latest .
docker run -p 7200:7200 -v /data:/opt/graphdb/home --name my-gdb1 graphdb:latest
docker save -o ../graph/graphdb.tar graphdb
