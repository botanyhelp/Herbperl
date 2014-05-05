#!/usr/bin/perl
# excel_maker.cgi - generate HTML tables
#this program makes an Excel spreadsheet, contacts a network server listening 
# on port 8888 on this machine (/var/www/cgi-bin/excel_server.cgi needs to be 
# running) and that server copies the recently created spreadsheet to a folder 
# readable by the webserver process.  Since this program needs to write a file 
# it needs to do so in a place that the user "apache" (on this CentOS Linux) 
# has write permissions.  This Linux (for some reason) will not allow an
# apache-writable directory under the webroot (nifty CentOS security trick). 
# For this reason, the program writes the spreadsheet to a file in /var/www/excel/,
# contacts the excel_server.cgi (which rsyncs the files in /var/www/excel/ with
# those in /var/www/html/excel), and then prints a helpful message to the web 
# user.  
#use strict;
#use warnings;
use CGI;
use Spreadsheet::WriteExcel;
use IO::Socket;
use DBI;
my $title = "excel_maker_incollectorname.cgi";
my $cgi= CGI->new();
print $cgi->header();
print $cgi->start_html(-title => $title, -bgcolor => "white");
my $dsn = "DBI:mysql:host=localhost;database=herbforty";
my $dbh = DBI->connect($dsn, "apache", "apachePASS") or die "cantconnect $!";
my $sth = $dbh->prepare("SELECT * FROM incollectorname");
$sth->execute();
#make workbook using process number:
my $workbook = Spreadsheet::WriteExcel->new("/var/www/excel/$$.XLS");
# Add a worksheet to our workbook:
my $sheet1 = $workbook->add_worksheet("xincollectorname");
#initialize the row and column variables, which are used to access current cell:
my $row=0;
my $col=0;
# Add a Format (formats make MSExcel spreadsheets have bold chars, wide columns, etc.):
my $format = $workbook->add_format();
$format->set_bold();
$format->set_size(15);
$sheet1->activate();
#START WHILE
while(my(@currentRow) = $sth->fetchrow_array()){
	foreach my $element (@currentRow) {
		#write the element to the next spreadsheet cell:
		$sheet1->write($row, $col, $element, $format);
		$col++;
	}
	#increment the row and reset the column to zero:
	$row++;
	$col=0;
#END WHILE
}

#We need to tell a process (that is not running as user apache) to move the file 
# to a location like /var/www/html/excel/ so that users can pick it up.  We cannot 
# run an every-minute cron job, because the user will want to download their 
# spreadsheet immediately, or nearly so, and so we want to tell another, listening 
# process to copy the file to /var/www/html/excel/ right away after the user 
# creates the file in apache-writable /var/www/excel (which users cannot get to). 
# All of this seems necessary because this linux won't make any directories 
# under /var/www/html owned by user apache, (chown apache /var/www/html/excel fails.)
#To do so, we'll setup a tcp client:
my ($host, $port, $handle);
$host = "127.0.0.1";
$port = 8888;
# create a tcp connection to the specified host and port
$handle = IO::Socket::INET->new(Proto     => "tcp",
                                PeerAddr  => $host,
                                PeerPort  => $port)
       or die "can't connect to port $port on $host: $!";

$handle->autoflush(1);              # so output gets there right away
#print STDERR "[Connected to $host:$port]\n";
#send the server the process ID so that it know to copy that file to /var/www/html/excel/
#...not working yet, so we're using system(rsync) to synchronize the folders:
print $handle "$$\n";
#$handle->send($$,
close($handle);
#at this point, /var/www/cgi-bin/excel_server.cgi has been contacted, and therefore it 
# is currently running 'rsync -r /var/www/excel/ /var/www/html/excel/', which will take 
# at least several seconds, so let's ask user to be patient, wait 30 seconds,
print("<B>Please wait 30 seconds while your spreadsheet is being created, then click on this link:...</b><BR>");
# and print the link to the newly-created spreadsheet:
print("<a href=\"/excel/$$.XLS\">Download Excel Spreadsheet $$.XLS</a>");
print $cgi->end_html();
exit (0);
__DATA__

ACCESSION
TYPE
COLLDATE
FLOWER
FRUIT
STERILE
OBJTYPE
INST
ANNCODE
ANNDATE
ANNSOURCE
CITY
SITENO
CITYTYPE
COLL2NAME
COLL3NAME
COLL1NAME
COLLNO1
COLLEVENT
TAXCD
CFS
CFV
CFVariety
HABITAT_MISC
HABITAT
LONGX
LAT
ELEV
LLGENER
LONG2
LAT2
LTDEC
LGDEC
NOWLOC
LOAN
PAGES
ORIGCD
PUBCD
LITCIT
PUBDATE
PUBDATEA
VERPERS
VERDATE
EX
ARTICLE
PREC
STATEL
COUNTY
COUNTRY
T1
R1
S1
NSEW_1
TRSGENER
T2
R2
S2
NSEW_2
PLACE
scan
MAPFILE
username
date_time
DTRS

