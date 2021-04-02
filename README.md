''' Project for representing covid dataset in knowledge graphs using graphDB '''


Please install all below pre-requisite in order to run the program:
    
	- pip install pandas
	- pip install rdflib
	- pip install configparser


Inside ontotext_new folder, we have two sub-folder (Screenshots and graph) and three files (one python file with name csv_to_rdf, another is path.properties file and last is turtle file with name rdf).

 Inside graph sub-folder we have:

        - Dockerfile which is used to run free version of GraphDB.

        - GraphDB zip file which is very important to run the current free version of GraphDB (9.6.0).

steps to follow: 

Download the ontotext_new folder on the desktop and do the following:

1. In graph sub-folder we have Dockerfile and graphdb zip file to build and run the image using commands:

        - docker build -t imagename:<tag> . 
        - docker run --publish 7200:7200 imagename 
  where imagename is the name that you want to the docker image it can be anything and generally its a good practice to use tags and also you can give any name to the tag.
  
Now, open the graphdb free version on the local host which we will get after running the docker. Once the graphdb is up, just create a repository with any id.

2. open path.properties file, it is a configuration file which is used to store the path variables vlues required while executing the python script. This will make our code more generic and ensure that no need to do any changes in the python file.There are total three path variables in path.properties file:
        
	- **url_path** : where we can simply pass the url of the csv file.
	- **rdf_path** : It can be used to store our rdf graph in turtle format locally. Although to run this program we don't require this variable path. So it is an optional,           just in case we want to store the turtle file locally we can use this path.
	- **graphdb_path** : This is the path of our repository in GraphDb, just specify http://localhost:7200/repositories/repository-id/statements where repositor-id is the id of the repository that you created in GraphDB.

NOTE: If you dont wish to store rdf locally then please remove **rdf_path** from path.properties and also comment out line number 26 and 237 in csv_to_rdf file and then use the files. As I was storing it locally just to see the contents in it that is why I used the paths but you can remove simply remove the paths if you dont want to store rdf file locally.

3. run csv_to_rdf python file. Now it take the url of the csv file and convert it into rdf format and store it into the GraphDB repository. Now we can run the queries against the Database.

4. Also we have rdf.ttl file which we created using python rdflib library, although its not require to store rdf file in turtle format locally as I said above, but in case if you want to have a look at it then you can store it otherwise our script will directly store rdf graph into GraphDB repository.

5. Finally, there is another folder named Screenshots, where you can see some of the queries that I ran and their results. Also, there is some other screenshots depicting some of the insights of the work (different classes, their relationship and so on).

Note: 


''' Steps that have been used to create docker image, container. '''

    - docker build -t graphdb:latest .
    - docker run -p 7200:7200 -v /data:/opt/graphdb/home --name my-gdb1 graphdb:latest
