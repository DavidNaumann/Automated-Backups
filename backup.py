from ftplib import FTP
from datetime import datetime
import os, sys, os.path
from shutil import make_archive, rmtree
from backup_functions import data_searcher, try_new_dir

print("Beginning backing up FTP server...")

# FTP OPTIONS

# IP for FTP server	
ip = '127.0.0.1'
# Username for FTP server
username = 'username'
# Password for FTP server
passwrd = 'password'

# Starting location on FTP server (basically where you want to start your backup)
# ALSO FROM ROOT !!! AND NEEDS TO EXIST
# For Windows example: "C:/Server_Backups/"
#
# Any other OS example: "/Server_Backups/"

starting_location = '/a/location/that/exists'


# HOST OPTIONS

# Stores if you want to zip the output folder (True = Zips folder, False = Does not zip folder)
zip_folder = True

# Backup location on host machine (basically where you want to store your backup)
# ALSO FROM ROOT !!! AND NEEDS TO EXIST
# For Windows example: "C:/Server_Backups/"
#
# Any other OS example: "/Server_Backups/"

backup_location = 'C:/also/a/location/that/exists'



'''	
-------------------------------------------------------------------
'''

# CLEANING INPUTS

# cleaning starting_location
last_char_pos = len(starting_location) - 1
last_char = starting_location[last_char_pos]
first_char = starting_location[0]
if last_char != '/':
	starting_location += '/'
if first_char != '/':
	starting_location = '/' + starting_location

# cleaning backup_location
last_char_pos = len(backup_location) - 1
last_char = backup_location[last_char_pos]
if last_char != '/':
	backup_location += '/'

'''	
-------------------------------------------------------------------
'''	

# BEGINNING PROCESS TO BACKUP

file_location = backup_location

try:
	os.chdir(file_location)
except:
	print(file_location + " does not exist!")
	sys.exit(1)

# Gets time of day to store for the backup
timeofday = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')

file_location += timeofday
file_location += '/'

os.mkdir(timeofday)
os.chdir(file_location)
		
# If not starting at root

if starting_location != '/':
	temp_location = starting_location
	last_pos = len(starting_location) - 1
	if temp_location[last_pos] == '/':
		temp_location = temp_location[:-1]
	last_slash = temp_location.rfind('/')
	temp_arr = temp_location.split('/')
	
	last_folder_pos = len(temp_arr) - 1
	temp_location = temp_arr[last_folder_pos]
	temp_location += '/'
	# Changes temp_location to new location after shift
	file_location += temp_location
		
	try:
		os.mkdir(temp_location)
		os.chdir(file_location)
	except:
		print("Could not make folder " + temp_location +"!")
		sys.exit(1)

currdir = starting_location

'''	
-------------------------------------------------------------------
'''

# BEGINS TO BACK UP FROM SERVER

print("Establishing connection to "+ ip + "...")

try:
	ftps = FTP(ip)
	ftps.login(user=username,passwd=passwrd)
except:
	print("Connection not established.")
	print("INCORRECT CREDENTIALS OR IP!")
	sys.exit(1)

# Begins to download files

print("Downloading files from " + ip + "...")
data_searcher(ftps,starting_location,currdir,file_location)

# Quits FTP server

ftps.quit()	
'''	
-------------------------------------------------------------------
'''

# FINISHES BY ZIPPING FOLDER (IF zip_folder SET)

if zip_folder:
	# Goes back to main back location by changing current directory

	file_location = backup_location
	os.chdir(file_location)

	# Zips folder for better space management

	print("Zipping files into " + timeofday + ".zip file...")
	make_archive(timeofday, "zip", timeofday)

	# Removes remaining folder

	print("Removing temporary folder")
	rmtree(timeofday)