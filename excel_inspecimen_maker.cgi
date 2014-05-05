#!/usr/bin/perl
# excel_inputspecimen_maker.cgi - generate HTML tables
use strict;
use warnings;
use CGI;
use Spreadsheet::WriteExcel;
use DBI;

#this tells the browser that an Excel spreadsheet is coming at them:
#print("Content-Type: application/vnd.ms-excel\n\n");
my $cgi = CGI->new();
print $cgi->header();
print $cgi->start_html();
my $title = "excel_inspecimen_maker.cgi";
my $dsn = "DBI:mysql:host=localhost;database=herbforty";
my $dbh = DBI->connect($dsn, "apache", "apachePASS") or die "cantconnect $!";
{ # begin scope

my $workbook = Spreadsheet::WriteExcel->new("/var/www/write_area/$$.xls");
my $worksheet = $workbook->addworksheet();
my $sth = "SELECT * FROM inspecimen";
$sth->execute();
#START WHILE
#while(my($ACCESSION, $Taxcd, $CFS, $CFV, $CFVariety, $PAGES, $OBJTYPE, $scan, $INST, $CITY, $STATEL, $COUNTY, $COUNTRY, $CITYTYPE, $SITENO, $PLACEOPEN, $TRSGENER, $T1, $R1, $S1, $NSEW_1, $LAT, $LONGX, $LTDEC, $LGDEC, $T2, $R2, $S2, $NSEW_2, $LAT2, $LONG2, $ELEV, $MAPFILE, $PREC, $HABITAT1, $HABITAT, $HABITAT_MISC, $COLLNO1, $COLLDATE, $COLL1NAME, $COLL2NAME, $COLL3NAME, $COLLEVENT, $ANNCODE, $ANNDATE, $ANNSOURCE, $TYPE, $FLOWER, $FRUIT, $STERILE, $LITCIT, $ARTICLE, $ORIGCD, $PUBCD, $PUBDATE, $PUBDATEA, $VERPERS, $VERDATE, $EX, $label_flg, $num_label_print, $validation_no, $validation_dt, $entry_done_flg, $username, $date_time) = $sth->fetchrow_array()){
my $row=0;
my $col=0;
while(my(@currentRow)=$sth->fetchrow_array()){
	foreach my $element (@currentRow) {
		#$worksheet->write($row, $col, $element);
		$col++;
	}
	$row++;
#END WHILE
}
$worksheet->write(0,0,"yo baby");
} # end scope
print $cgi->end_html();
$dbh->disconnect ();
exit (0);
