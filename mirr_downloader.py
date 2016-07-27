#! /usr/bin/python

import getopt
import os
import ftplib
import sys
import getpass
import zipfile
import shutil

from ftplib import FTP_TLS as FTP
from fnmatch import fnmatch
from threading import Thread

recursive = False
host = ""
username = "anonymous"
password = None
pattern = ""
remote_dir = "/"
local_dir = os.getcwd()
compress = False
DOWNLOAD_FOLDERS_NAME = "Downloads"

def usage():
	print "Usage: python mirr_downloader.py [-?] [[-r] [-z] [-l username -p] [-f remote_dir] [-d local_dir] [-s regex] host]\n"
	print "-?: \t\t\t\tShow this helper."
	print "-r: \t\t\t\tRecursive. Download all folders content. Default = False"
	print "-u username: \t\t\tUsername to connect to the specified FTP host. Default = anonymous."
	print "-p : \t\t\t\tPassword associated with the specified username, if any."
	print "-s: \t\t\t\tExclude files and directories that match the specified regular expression"
	print "-z: \t\t\t\tGet a compressed version of the files. Default = False"
	print "-h remote_dir: \t\t\tRemote dir from which downloading content. Default = / (root)."
	print "-l local_dir: \t\t\tLocal dir where save downloaded files. Default = actual directory."
	print "\n\033[1m\033[91mInfo\033[0m: \033[1mbolded and underlined elements are for folders.\033[0m"
	sys.exit(0)

def scan_arguments():
	global recursive, host, username, password, pattern, compress, remote_dir, local_dir
	try:
		opts, args = getopt.getopt(sys.argv[1 : ], "h:l:prs:u:z?")
	except getopt.error:
		usage()

	for o, a in opts:
		if o == "-?":
			usage()
		elif o == "-r":
			recursive = True
		elif o == "-u":
			username = a
		elif o == "-p":
			password = getpass.getpass(prompt="Password: ")
		elif o == "-s":
			pattern = a
		elif o == "-z":
			compress = True
		elif o == "-h":
			remote_dir = a[:-1] if a[-1] == "/" else a		#Remove last trailing "/"
		elif o == "-l":
			if not os.path.exists(a):
				print "The local path '{0}' doesn't exist.".format(a)
				sys.exit(0)
			elif not os.path.isdir(a):
				print "The local path '{0}' must be a directory path.".format(a)
				sys.exit(0)
			else:
				local_dir = a[:-1] if local_dir[-1] == "/" else a		#Remove the final "/" from the local path since it's added from the remote path

	if not args:
		print "Hostname missing.\n"
		usage()
	elif username != "anonymous" and password is None:
		print "You need a password to access if you specify a username."
		sys.exit(0)
	else:
		host = args[0]

def is_file(file_name):
	try:
		ftp_client.cwd(file_name)
	except ftplib.all_errors:
		return True
	else:
		ftp_client.cwd("..")
		return False

def print_directory_content(files):
	print "\nFiles in the remote path '{0}'\n".format(remote_dir)
	for file in files:
		if is_file(file):
			output = "-"
		else:
			output = "\033[1m\033[4m+"
		output += " {0}\033[0m".format(file)
		print output
	print ""

def setup_folder():
	global local_dir

	if local_dir == os.getcwd() or local_dir[-1:] != "/":
		local_dir += "/{0}".format(DOWNLOAD_FOLDERS_NAME)
	else:
		local_dir += "{0}".format(DOWNLOAD_FOLDERS_NAME)

	if not os.path.exists(local_dir):
		os.makedirs(local_dir)

def download_files(base_path, files):

	saving_path = local_dir + "{0}".format(base_path)

	if not os.path.exists(saving_path):
		os.makedirs(saving_path)

	for file in files:
		file_name = base_path + "/" + file

		if fnmatch(file, pattern):
			print "--- {0} skipped.".format(file_name)
			break

		try:
			is_f = is_file(file)
			if is_f:
				print "\n*** Downloading content of '{0}'".format(file_name)
				file_path = saving_path + "/" + file
				with open(file_path, "wb") as fi:
					ftp_client.retrbinary("RETR " + file, lambda data: fi.write(data))
				print "Saved in '{0}'\n".format(file_path)
			elif not is_f and recursive:
				inner_directory = file_name
				try:
					ftp_client.cwd(inner_directory)
					print "--> Switched working directory to : " + inner_directory
					rec_files = ftp_client.nlst()
				except ftplib.all_errors as e:
					print "ERROR: cannot fetch files list for remote directory '{0}'. Message returned from server:".format(inner_directory)
					print e
				else:
					print "\n+++ Downloading recursively content of '{0}'".format(inner_directory)
					download_files(file_name, rec_files)
					ftp_client.cwd("..")
					print "<-- Restored working directory to " + base_path
			elif not is_f and not recursive:
				print "\n--- Skipping '{0}': folder and not recursive mode.".format(file_name)
		except ftplib.all_errors as e:
			print e
			print "ERROR: cannot download '{0}'. Other downloads will continue.".format(file)

def create_zip(path):
	real_path = path.split("/")[-1]
	print "Creating zip..."
	zip = zipfile.ZipFile(DOWNLOAD_FOLDERS_NAME + '.zip', 'w', zipfile.ZIP_DEFLATED)
	for root, dirs, files in os.walk(real_path):
		for file in files:
			zip.write(os.path.join(root, file))
	zip.close()
	print "Zip created. Cleaning up useless resources..."
	shutil.rmtree(path)

def main():
	global ftp_client

	scan_arguments()
	ftp_client = FTP(host)

	try:
		ftp_client.login(username, password)
	except ftplib.all_errors as e:
		print "ERROR: cannot login with username '{0}' and relative password.\nMessage returned from server:".format(username)
		print e
		return

	try:
		ftp_client.cwd(remote_dir)
	except ftplib.all_errors as e:
		print "ERROR: emote directory '{0}' not existing.\nMessage returned from server:".format(remote_dir)
		print e
		return
	else:
		files = ftp_client.nlst()
		print_directory_content(files)
		setup_folder()
		download_files(remote_dir, files)
		if compress:
			create_zip(local_dir)

	try:
		ftp_client.close()
		print "!!!!! OPERATION COMPLETED SUCCESSFULLY !!!!!"
	except ftplib.all_errors as e:
		print "ERROR: cannot close the connection properly.\nMessage from server:"
		print e

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print "\nOperation canceled. Bye."