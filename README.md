''' Project for representing covid dataset in knowledge graphs using graphDB '''


Please install all requirements in order run the program:
    
	- pip install pandas
	- pip install rdflib
	- pip install configparser


Inside ontology folder, we have two sub-folder (screenshots and graph) and three files (one python file with name csv_to_rdf, another is path.properties file and last is turtle file with name rdf).

 Inside graph sub-folder we have:

        - Dockerfile which is used to run free version of GraphDB.

        - GraphDB zip file which is very important to run the current free version of GraphDB (9.6.0).

steps to follow: 

Download the ontology folder on the dektop and do the following:

1. In graph sub-folder we have Dockerfile and graphdb zip file to build and run the image using commands:

        - docker build -t imagename:<tag> . 
        - docker run --publish 7200:7200 imagename 
  where imagename is the name that you want to the docker image it can be anything and generally its a good practice to use tags and also you can give any name to the tag.
  
Now, open the graphdb free version on the local host which we will get after running the docker. Once the graphdb is up, just create a repository with any id.

2. open path.properties file, it is config file where we can pass all the paths so that we dont need to search the paths inside our python file. We have three paths in path.properties file:
        
	- First path is url_path where we can simply pass the url of the csv file.
	- Second path which is rdf_path can be used to locally store our rdf graph in turtle format. Although to run this program we dont require second path. So it is optional,           just in case you want to store the turtle file locally.
	- Third path is the path of our repository in GraphDb, just specify http://localhost:7200/repositories/repository-id/statements where repositor-id is the id of the                 repository that you created in GraphDB.

3. In csv_to_rdf python file first specify the path of path.properties file and run it. Now it take the url of the csv file and convert it into rdf format and store it into the GraphDB repository. Now we can run the queries against the Database.

4. Also we have rdf.ttl file which we created using python rdflib library, although its not require to store rdf file in turtleformat locally as I said above, but in case if you want to have a look at it then you can store it otherwise our script will directly store rdf graph into GraphDB repository.

5. Finally, there is another folder named screenshots, where you can see some of the queries that I ran and their results. Also, there is some other screenshots depicting some of the insights of the work (different classes, their relationship and so on).

Note: 


''' Steps that have been used to create docker image, container. '''

    - docker build -t graphdb:latest .
    - docker run -p 7200:7200 -v /data:/opt/graphdb/home --name my-gdb1 graphdb:latest
