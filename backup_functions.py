from ftplib import FTP
from datetime import datetime
import os, sys, os.path
from shutil import make_archive, rmtree

'''

Function data_searcher()

Description: Recursively gets files from the server

Inputs:
ftps = current FTP connection made in main file
starting_location = Where the server is starting from (ex. "/" would be root, "/this_folder/" would be up one folder from root)
currdir = is where the recursion is currently at folder wise
file_location = where the file is being stored

Output:
The files in the correct location

'''

def data_searcher(ftps, starting_location, currdir,file_location):
	olddir = currdir
	temp_file_location = file_location
	if currdir != starting_location:
		try_new_dir(temp_file_location)
	os.chdir(file_location)
	filenames = ftps.nlst(currdir)
	ftps.cwd(currdir)
	for filename in filenames:
		is_directory = filename.find('.')
		if is_directory == -1:
			currdir += filename
			currdir += '/'
			temp_file_location += filename
			temp_file_location += '/'
			data_searcher(ftps, starting_location, currdir,temp_file_location)
			temp_file_location = file_location
			currdir = olddir
			ftps.cwd(currdir)
		else:
			local_filename = os.path.join(file_location,filename)
			file = open(local_filename, 'wb')
			ftps.retrbinary('RETR ' + filename, file.write)
			file.close()
	return


'''

Function try_new_dir()

Description: Trys making new directory

Inputs:
currdir = directory that needs to be made

Output:
A new directory or an error stating that the directory already exists

'''
	
def try_new_dir(currdir):
	try:
		os.makedirs(currdir)
	except FileExistsError:
		print("Directory " , currdir ,  " already exists")
	return