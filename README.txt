This application has been developed to be a prototype for diagnostic centre management system.

!!!! Please ensure that you have installed the prerequisites mentioned below !!!!

TEAM NAME         :REBORN
TEAM MEMBERS :    Mukesh Padmanabhan, Niranjan Balakumar, Aswin

PRE-REQUISITES :
	+Python - 3.7 or higher
	+MySQL-8.0 or higher (Usage of WAMP is discouraged due to potential DLL errors)
	+Ensure that you have installed mysql.connector module 
	 (Installed Python-MySQL connector version >=8.0) or
	 pymysql module along with the necessary DLL files. 
	+Extract the 4 files(3 Text Doc and 1 Python Script) from the archive and store them in the SAME folder before use.

WORKING:
	+Ensure MySQL server is running.
	+The application is user friendly and users are guided throughout.
	+Two user levels- Admin and Doctor have been designed.

	+Admins can:
	>View, add, modify or delete doctors and patients data.
	>Search for doctors on the basis of Medical License Number/Centre ID/Name/Contact Number.
	>Search for patients on the basis of Registration Number/Name/Phone Number.
	>Add more titles(duty type) for doctors.
	>Add more tests  for patients.

	+Doctors can:
	>View, add, modify or delete patients data.
	>Search for patients on the basis of Registration Number/Name/Phone Number.
	>Add more tests  for patients.

	+Dedicated login window handles user login.
	+Administrator Password is 'rockstaradmin'. It can be changed in the python code in line 876.
	+Doctor Password is 'rockstardoctor'. It can be changed in the python code in line 948.
	+On startup, a window asks for the MySQL database credentials. Certain pre-existing values are assigned which can be replaced.
	+Users are asked not to tamper with the files 'Doctor File' and 'Patient File'. Even renaming these files may lead to errors.
	+It is because they are the flat files which store the data for doctors and patients. They are automatically updated at the end of each session.
		
	
		
