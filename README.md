The docker-compose starts all the docker containers that are involved in the digione project. It starts rabbitMQ, anonymizer, radiomics, xnat_listener send_xnat, xnat-db, xnat-ngix, nxat web. The config.yaml file creates queues in rabbitMQ, this file is shared with the containers via the volumes. It also tells you which queue needs to be used to send the next message when a container has completed his message. When changing titles in the config file makes sure that these are also changed in corresponding repositorie scripts.

The pipeline works as follows: send a message via rabbitMQ to the anonymizer, in this message is the inputfolder, which should correspond to the same folder in the anonymizer volume, and a outputfolder. This outputfolder should also correspond to a local folder via a volume. The anonymizer, anonymizes based on the recipes in anonymiser_recipes folder, it then creates a new rabbitMQ message which sends folder path to the send_xnat queue. This next container saves the data in xnat. The xnat_listener checks xnat for new data in xnat when it detects new dat is sends a message to the radiomics queue. This calulcates the radiomics features (I have not been able to confirm that the results from this are correct), it again send a new message to the send_xnat container with the folder, where the the CSV radiomics. This saeves the radiomics csv in xnat. Becareful that when changing folder_paths that this also correctly done in the volume part of the docker-compose file. For extensive explanations look at the readME in the repositories.

Important things to know:
- When changing the XNAT projects make sure that the AE title of the SCP reveiever matches the ID of the project. Right now it is filtered based on hard coded values in the send_XNAT_data repository.
- The anonymiser repository automtically deletes all the files in the folder where the new anonymised files will be saved.
- If a patients ID is not in the patient-lookup.csv it automatically stops and will not be send to XNAT
- The XNAT_listener checks right only if a new patient is detected. So if a patient gets a second study it will not detect this. However, this will be solved with a postgres database that will be added with the storeSCP.

XNAT:
-The site is setup that the labels in the projects correspond to the study instance UID. This way if one patient haas multiple studies it categorizes based upon the study UID.

Needs to be done:
-I build the send_xnat container from a repository from TomSinsel, this should be an mdw-nl repostiory maybe the xnat. This has been tried by adding the send_xnat folder to the repository. But it has errors with submodules.
-Right now in the send_xnat_data repository the way files are sorted to certain projects in xnat is hard coded in the BodyPartExamined tag. When its clear which identifier it should be it should be changed.
-Maybe a way to change some url in the digione infrastructure repository
-Change in the start_up.sh script in the xnat repository so that it waits longer before executing the configure_XNAT.py script, sometimes it tries to run the API calls for site_setup and the SCP receiver before they can be run.
-DICOM anonymiser -> build patient_lookup.csv with the SCP?
-DICOM anonymiser -> patient droppen if not in the patient_lookup.csv ✔
-DICOM anonymiser -> org_id needs to be a setting in the dicom infrastructure now it its set for every uuid manually in the recipe.dicom file and better documentation
-Pop the message in the rabbitmq queue before it is executed ✔
-Anonymizer -> XNAT -> Radiomics ✔
-Implement a storeSCP before the pipeline
-Radiomics op study niveau -> Study waar RTStruct staat ✔
-Anonymizer/Radiomics/sendXNAT containers have all the functionality in one script make for these an extra script that runs everything
