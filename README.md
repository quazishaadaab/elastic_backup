ELK Backup V2
The ELK Backup V2 Epic is responsible for backing up our watchers, logstash pipelines, and ILM ( index lifecycle management policies). The V2 backup is different from the V1 backup ( https://gitlab.int.bell.ca/tvsre-tools/elastic/elk-application-execution/-/blob/master/ElasticBackup.py) because it uses an object oriented approach. This OOP approach allows us to break down the critical steps into 4 functions, which makes it easier to understand and visualize the code. The V1 Elk Backup may be more difficual and harder to read/understand because everything is happening all at once. In the V2 , critical steps are 1)taking a snapshot 2) getting backup config data 3) parsing the backup data and 4) pushing it to gitlab.

STEP 1 : CREATNG THE SNAPSHOT OBJECT
The first step involves creating a snapshot object that is unique to the data type we want to backup ( watchers or logstash pipelines or ILM). This object has all the methods and variables required to do steps 2,3, and 4 ( getting backupdata , parsing it, and pushing it to github).

STEP 2 : TAKING THE SNAPSHOT
Step 2 involves using a get request to load up all the unfiltered backup data pertaining to the data type in question( watcher, logstash, or ILM) . This snapshot will initialize the instance variables of the object created in step 1. The elastic_url instance variable will be initialized and have a value of the elastic API url for the data type. The gitlab_url instance variable will be intialized to the gitlab project url for the data type. In addition, the unfiltered backup data will be stored in the variable , backup_data.

STEP 3 : PARSING THE BACKUP DATA
Step 3 involves cleaning the unfiltered backup data and storing it in a proper directory. Each data type has a different way of cleaning the unfiltered data due to extra unique config info pertaining to each data type. Once the data is cleaned , a json file is created under the name of the watcher,logstash pipeline, or ILM policy it belongs to. These json files are then grouped into a directory under the name of the data type . Watcher files will in the watcher-backup directory , ILM policy data will go under the ILM folder, and logstash pipeline config data will go under the logstash folder.

STEP 4 : PUSHING TO GITLAB
Step 4 involves pushing the directories and its files to the proper gitlab project. This happens by running commands on the terminal .
