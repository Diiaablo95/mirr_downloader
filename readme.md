# What is it?

Small script to download files from an FTP server using SSL connection, like already a looot of scripts do.

# Why did I do this?
I implemented it as an exercise taken from the book "Core Python Applications Programming 3rd edition by Wesley J. Chun" at the end of the chaper 3 about internet programming. I found the exercise very interesting altough very primitive.

#How does it work?
Its working is very simple, and it takes as reference the already well-know <a href = "http://svn.python.org/projects/python/trunk/Tools/scripts/ftpmirror.py">ftpmirror.py</a>.
The only difference, is that my script doesn't do, at the moment, a lot of things the script does, but it gives the chance to zip the downloaded files.

## Usage

After having downloaded the script and changed the working directory to the one containing it wherever you have moved it, grant it execution privileges to the file (<strong><code>chmod +x mirr_downloader.py</code></strong>) and execute the following command through the command line:
<strong><code>./mirr_downloader.py mirr_downloader.py [-?] [[-r] [-z] [-l username -p] [-f remote_dir] [-d local_dir] [-s regex] host]</code></strong>

<ul>
<li><strong>-?</strong> : Show the helper screen;</li>
<li><strong>-r</strong> : <i>recursive mode</i>. Download content of directories found in the specified path and its subdirectories as well;</li>
<li><strong>-z</strong> : <i>zip download</i>. After having downloaded the files, a zip called Downloads.zip is created in the specified local path;</li>
<li><strong>-l</strong> : <i>ftp account username</i>. Username used to log into the ftp. <i>By default it's set to anonymous</i>;</li>
<li><strong>-p</strong> : <i>ftp account password</i>. If username is specified, than password is required. It has to be prompted after having launched the command, like most of programs (e.g. ssh) does;</li>
<li><strong>-f</strong> : <i>remote directory root path</i>. The path from which to start downloading the files. All the files will be downloaded and, if recursive mode is enabled, all the subfolders content as well;</li>
<li><strong>-d</strong> : <i>local directory</i>. Path where to store downloaded files. A folder call "Downloads" will be create as a container for all the downloaded files. <i>By default, it's created in the same path from where as the script is <strong>launched</strong></i>;</li>
<li><strong>-s</strong> : <i>regex skip</i>. Specify a regex to evaluate file names to skip. <i>E.g. *.jpg will not download any jpg file</i>;</li>
<li><strong>host</strong> : FTP host from which download content;</li>
</ul>

## Future improvements

I have already written down something for the future:
<ul>
<li><strong>Multi-threading</strong>: I have tried to implement a parallel upload solution, but I got some errors. I want to understand if it's due to my FTP host or it's a bug in the script;</li>
<li><strong>Upload feature</strong>: in the same way in which downloading files is possible, I would like the feature to upload files to the server as well;</li>