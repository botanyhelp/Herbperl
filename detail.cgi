#!/usr/bin/perl
# detail.cgi - wisflora specimen records listing
#use strict;
#use warnings;
use CGI;
use DBI;
use URI::URL;
my $title = "detail.cgi";
my $cgi = new CGI();
print $cgi->header(); 
print $cgi->start_html(-title => $title, -bgcolor => "white");
my $dsn = "DBI:mysql:host=localhost;database=herbfortynine";
my $dbh = DBI->connect($dsn, "apache", "apachePASS") or die "cantconnect $!";
my $SpCodeParam = $cgi->param("SpCode");
my $GenusParam = $cgi->param("Genus");
my $FamilyParam = $cgi->param("Family");
my $SpeciesParam = $cgi->param("Species");
my $CommonParam = $cgi->param("Common");
#synonym_printed is a flag to tell us whether to print 
# the "Synonyms" heading to be followed by synonyms:
my $synonym_printed = 0;
my $thumbmapsstring;
my $handstring;
my $dotmapsstring = '';
my $handParam = $cgi->param("hand");
my $hand = $handParam;
#construct the url for the hand maps...if there is one, then "$hand" now holds 'H', which we substitute:
$hand=~s/H/\/herb\/wwwbotanydev\/herbarium\/wisflora\/hand\/$SpCodeParam.gif/g;
my $thumbmapsParam = $cgi->param("thumbmaps");
my $thumbmaps = $thumbmapsParam;
$thumbmaps=~s/\.\.\//\/herb\/wwwbotanydev\/herbarium\/wisflora\//g;
$thumbmapsstring = $thumbmaps;
my $hand_url = '';
my $hand_exists = 0;
my $dot_url = '';
my $dot_exists = 0;
my $thumb_url = '';
my $thumb_exists = 0;
my $usda = '';
my $usda_exists = 0;
my $usda_url = '';
#these are control flags to control family info output
my $first_loop_flag = 0;
my $first_loop_flag_two = 0;
my $first_loop_flag_three = 0;
#array to hold photos (i.e. records in link table with "Type" field values of "3"
my @photos = ();
#array to hold nonphotos (i.e. records in link table with "Type" field values NOT of "3"
my @nonphotos = ();

# these three variables can hold data from the Syncd="." canonical spdetail record:
my $Photo = "";
my $Photographer = "";
my $Thumbphoto = "";
#these few varibles will store the genus and species information where spdetail:Syncd = ".":
my $Genus;
my $Species;
my $Common;
my $Family;

#I'd rather not declare these "global" my variables...instead, I'd rather have this "my" clause 
# used inside of a while( ) loop, like ''while(my ($spdetail_Taxcd...) = $sth->fetchrow() ){ }'' 
# for now I think the only reason I need to do this is because I'm needing it at the end of the 
# webpage-making process, where google-maps links refer to $spdetail_genus, for example, but 
# that variable had gone out of scope (when we make google links far below).  
my ($spdetail_Taxcd, $spdetail_Syncd, $spdetail_family_code, $spdetail_genus, $spdetail_species, $spdetail_authority, $spdetail_subsp, $spdetail_variety, $spdetail_forma, $spdetail_subsp_auth, $spdetail_var_auth, $spdetail_forma_auth, $spdetail_sub_family, $spdetail_tribe, $spdetail_common, $spdetail_Wisc_found, $spdetail_ssp, $spdetail_var, $spdetail_f, $spdetail_hybrids, $spdetail_status_code, $spdetail_hide, $spdetail_USDA, $spdetail_COFC, $spdetail_WETINDICAT, $spdetail_FAM_NAME, $spdetail_FAMILY, $spdetail_GC, $spdetail_FAMILY_COMMON, $spdetail_SYNWisc_found, $spdetail_SYNS_STATUS, $spdetail_SYNV_STATUS, $spdetail_SYNF_STATUS, $spdetail_SYNHYBRIDS_STATUS, $spdetail_SYNW_STATUS, $spdetail_speciesweb_Taxcd, $spdetail_Status, $spdetail_Photo, $spdetail_Photographer, $spdetail_Thumbmaps, $spdetail_Accgenus, $spdetail_SORTOR, $spdetail_Hand, $spdetail_growth_habit_bck, $spdetail_blooming_dt_bck, $spdetail_origin_bck, $spdetail_Thumbphoto, $spdetail_date_time, $spdetail_growth_habit, $spdetail_blooming_dt, $spdetail_origin, $spdetail_Taxa, $spdetail_spdetail_id);

















{ # begin scope
	# run queries...
	my $sth = $dbh->prepare ("SELECT * FROM spdetail WHERE Taxcd = '$SpCodeParam' ORDER BY Syncd");
	my $sthtwo = $dbh->prepare ("SELECT * FROM link WHERE Taxcd = '$SpCodeParam' ORDER BY Type, Taxcd, Link");
	my $sththree = $dbh->prepare ("SELECT * FROM habitat WHERE Taxcd = '$SpCodeParam'");
	my $sthfour = $dbh->prepare ("SELECT ACCESSION, TYPE FROM specimen WHERE Taxcd = '$SpCodeParam' AND scan = '1'");
	$sth->execute();
	$sthtwo->execute();
	$sththree->execute();
	$sthfour->execute();
#start looping through the link table query results:
 	while(my ($Type, $Taxcd, $Link, $Title, $Description, $link_id) = $sthtwo->fetchrow_array()) {
		#the following tests each examine the $Type field.  This field indicates what types of extra files are
		# available, be they photos, bigphotos, handmaps, thumbmaps, dotmaps, floristicRating, and more.  I 
		# currently don't know what all the codes mean, as there is no "legend" or "key" for me to know that, 
		# for example, that a $Type value in table 'link' of '3' means there is a photo available.  
		#more practically, this detail.cgi page needs to display images and links and floristic ratings, and 
		# the "Type" field in link has a value, like '3', that means something.  For example, if link has a 
		# record of "Type" "3", then the "Link" field likely holds filesystem info about where the file is 
		# located, perhaps "../images/photos/RUEHUM.jpg" or something.  
		#Many records have multiple photos, and so keep them all in @photos while we're looping:
		if($Type=~/3/){
			push(@photos, $Link, $Title, $Description);
		}elsif($Type=~/1a/){
			$dotmapsstring = "<a href=\"/herb/wwwbotanydev/herbarium/wisflora/dots/$SpCodeParam.gif\"><img src=\"/herb/wwwbotanydev/herbarium/wisflora/thumbmap/$SpCodeParam.gif\"></a><br><a href=\"/herb/wwwbotanydev/herbarium/wisflora/dots/$SpCodeParam.gif\">View specimen location map</a>";
			$dot_url = "<a href=\"/herb/wwwbotanydev/herbarium/wisflora/dots/$SpCodeParam.gif\">$Title</a><font size=-1>$Description</font>";
			$dot_exists = 1;
		}elsif($Type=~/1b/){
			$handstring = "<a href=\"/herb/wwwherbarium/wisflora/pictures/handmap/$SpCodeParam.gif\"><img src=\"/herb/wwwbotanydev/herbarium/wisflora/thumbmap/$SpCodeParam.gif\"></a><br><a href=\"/herb/wwwherbarium/wisflora/pictures/handmap/$SpCodeParam.gif\">View specimen location map</a>";
			$hand_url = "<a href=\"/herb/wwwherbarium/wisflora/pictures/handmap/$SpCodeParam.gif\">$Title</a> <font size=-1> $Description</font>";
			$hand_exists = 1;
		}elsif($Type=~/4/){
			my $fourstring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $fourstring);
			#true
		}elsif($Type=~/4a/){
			my $fourastring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $fourastring);
			#true
		}elsif($Type=~/4b/){
			my $fourbstring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $fourbstring);
			#true
		}elsif($Type=~/4c/){
			my $fourcstring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $fourcstring);
			#true
		}elsif($Type=~/4d/){
			my $fourdstring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $fourdstring);
			#true
		}elsif($Type=~/4g/){
			my $fourgstring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $fourgstring);
			#true
		}elsif($Type=~/4s/){
			my $foursstring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $foursstring);
			#true
		}elsif($Type=~/5x/){
			#true
			my $fivexstring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $fivexstring);
			$usda = $spdetail_USDA;
			$usda_url = "<a href=\"http://plants.usda.gov/cgi_bin/plant_profile.cgi?symbol=$usda\">USDA Plants Database</a>";
			$usda_exists = 1;
		}elsif($Type=~/6/){
			my $sixstring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $sixstring);
			#true
		}elsif($Type=~/6g/){
			my $sixgstring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $sixgstring);
			#true
		}elsif($Type=~/6h/){
			my $sixhstring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $sixhstring);
			#true
		}elsif($Type=~/6i/){
			my $sixistring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $sixistring);
			#true
		}elsif($Type=~/6j/){
			my $sixjstring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $sixjstring);
			#true
		}elsif($Type=~/7/){
			my $sevenstring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $sevenstring);
			#true
		}elsif($Type=~/8/){
			my $eightstring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $eightstring);
			#true
		}elsif($Type=~/8a/){
			my $eightastring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $eightastring);
			#true
		}elsif($Type=~/9/){
			my $ninestring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $ninestring);
			#true
		}elsif($Type=~/9a/) {
			my $nineastring = "<a href=\"$Link\"> $Title </a><ul><li> $Description </li></ul>";
			push(@nonphotos, $nineastring);
			#true
		}else{
			#nonthing in Link?
			print("<BR>HOLY COW, no Link table records<br>");
		}
		#END link record loop
	}
#start looping through the spdetail table query results:
#notice that there is no longer any spdetail_id and therefore it is not used?...perhaps 
# we should look over DBI error handing again, and start using RaiseError and whatnot.
 	while (($spdetail_Taxcd, $spdetail_Syncd, $spdetail_family_code, $spdetail_genus, $spdetail_species, $spdetail_authority, $spdetail_subsp, $spdetail_variety, $spdetail_forma, $spdetail_subsp_auth, $spdetail_var_auth, $spdetail_forma_auth, $spdetail_sub_family, $spdetail_tribe, $spdetail_common, $spdetail_Wisc_found, $spdetail_ssp, $spdetail_var, $spdetail_f, $spdetail_hybrids, $spdetail_status_code, $spdetail_hide, $spdetail_USDA, $spdetail_COFC, $spdetail_WETINDICAT, $spdetail_FAM_NAME, $spdetail_FAMILY, $spdetail_GC, $spdetail_FAMILY_COMMON, $spdetail_SYNWisc_found, $spdetail_SYNS_STATUS, $spdetail_SYNV_STATUS, $spdetail_SYNF_STATUS, $spdetail_SYNHYBRIDS_STATUS, $spdetail_SYNW_STATUS, $spdetail_speciesweb_Taxcd, $spdetail_Status, $spdetail_Photo, $spdetail_Photographer, $spdetail_Thumbmaps, $spdetail_Accgenus, $spdetail_SORTOR, $spdetail_Hand, $spdetail_growth_habit_bck, $spdetail_blooming_dt_bck, $spdetail_origin_bck, $spdetail_Thumbphoto, $spdetail_date_time, $spdetail_growth_habit, $spdetail_blooming_dt, $spdetail_origin, $spdetail_Taxa, $spdetail_spdetail_id) = $sth->fetchrow_array ()){
		#if the $spdetail_Syncd is equal to '.', then this is the canonical record, 
		# and so gather data from its bountiful fields:
		if($spdetail_Syncd eq ".") {
			#I might consider saving information about whether these 
			# assignments were successful or not, because it affects 
			# the outcome of the page:
			$Photo = $spdetail_Photo;
			$Photographer = $spdetail_Photographer;
			$Thumbphoto = $spdetail_Thumbphoto;
			$Genus = $spdetail_genus;
			$Species = $spdetail_species;
			$Common = $spdetail_common;
			$Family = $spdetail_FAMILY;
		}
		if($first_loop_flag == 0){





print <<"HEADER";
<table width="100%" border="0" bgcolor="#EEEEEE">
  <tr bgcolor="#E7E7B6">
    <td width="100%" bgcolor="#E7E7B6"><font color="#990000"><font size=+3>W</font><b><font size=+1>ISCONSIN </font></b><font size=+3>B</font><b><font size=+1>OTANICAL </font></b><font size=+3>I</font><b><font size=+1>NFORMATION </font></b><font size=+3>S</font><b><font size=+1>YSTEM</font></b></font></td>
  </tr>
  <tr>
    <td><table width="100%" border=0>
        <tr>
          <td width="400%" colspan="4" bgcolor="#A9BB97">
            <table width="100%">
              <tr>
                <td width="30%"> <b><i><font color="#990000" size="4">Wisconsin State Herbarium</font></i></b> </td>
                <td width="40%" align="center" VALIGN="middle">
                <p><font size="4"><b>Wisflora - Vascular Plant Species</b></font></p></td>
                <td VALIGN="CENTER" width="30%">
                  <div align="right"> <b><font size="-1">University of&nbsp; Wisconsin - Madison&nbsp;</font></b> </div></td>
              </tr>
          </table></td>
        </tr>
    </table></td>
  </tr>
</table>
<table width="100%" border="0">
  <tr bgcolor="#EEEEEE">
    <td align="center" width="25%">
      <p><strong>Menu:</strong> <font size=2><a href="/herbarium/"><b>Herbarium Home</b></a></font> </p></td>
    <td align="center" width="25%"> <font size="2"><a href="/wisflora/"><b>WISFLORA: Vascular Plant Species</b></a></font></td>
    <td align="center" width="25%"> <font size="2"><a href="/herb/search.html"><b>Vascular Plant Taxon Search</b></a></font> </td>
    <td align="center" width="25%"> <font size="2"><a href="/herb/specimenSearch.html"><b>Search Specimen Database</b></a></font> </td>
  </tr>
</table>
HEADER








print <<"TABLEZERO";
<TABLE width="100%"  border="0">
        <tr>
                <td width="60%">
                <TABLE width="100%" BORDER=0>
                        <TR>
                                <TD Align="Left">
                                <TABLE width="100%" BORDER=0>
                                        <TR>
                                                <TD width="33%" rowspan=2 ALIGN="center" VALIGN="middle">

TABLEZERO

	#be sure we only run this loop once:
	$first_loop_flag = 1;
	# see if there is any maps at all...
	if($spdetail_Thumbmaps=~/\.\./){
		#dotmap...if we have a dotmap, print it out!
		if($dotmapsstring=~/href/) {
			print("$dotmapsstring");
		#handmaps...else,if we have a handmap, print it out!
		}elsif($handstring=~/href/) {
			print("$handstring");
		}else{
			$thumbmapsstring .= $SpCodeParam;
			$thumbmapsstring .= ".gif";
			#print("$thumbmapsstring");
			#print("THUMB<BR>");
		}
	}








print <<"TABLETWO";
				&nbsp;
				</TD>
				<TD width="67%" ALIGN="CENTER" VALIGN="TOP">
				&nbsp;
TABLETWO





	if($FamilyParam ne ""){
		print $cgi->p("Family: $FamilyParam \n");
	}elsif($spdetail_common ne ""){
		#otherwise we can print what the database returns:
		print $cgi->p("Family: $Family\n");
	}else{
		#No Family name, so print nothing at all:
		;
	}
	my $tax = getTaxonNm($spdetail_Taxcd, $spdetail_Syncd);
	print $cgi->p("Taxon: $tax\n");
	if($CommonParam ne ""){
		#if we're called by a form, we can put what the user entered, may not be right:
		print $cgi->p("Common: $CommonParam \n");
	}elsif($spdetail_common ne ""){
		#otherwise we can print what the database returns:
		print $cgi->p("Common: $Common\n");
	}else{
		#No common name, so print nothing at all:
		;
	}
		
	
	if($spdetail_hide ne "") {
		#if hide field is not blank, that means 
		# this species is endangered and 
		# thus should not have any location 
		#information on the specimen page 
		# result, but this page is unaffected, 
		#so don't do anything, leave commented:
		#print $cgi->p("$spdetail_hide\n");
		;
	}
	#if $spdetail_Status matches "Excluded" print out a link to Excluded page
	if($spdetail_Status =~/Excluded/) {
		print("<BR>");
		print $cgi->a({-href=>"/Excludedtaxa.asp"}, "[Excluded]");
		print("<BR>");
	# otherwise print out meta-dat about species:
	}else{
		#If there is a Status and its not "Excluded, printout stuff:
		if($spdetail_Status eq '') {
			#since we have a non-"Excluded" Status field, that 
			#means other fields exist, if they do, we can printout.
			#if origin, printout
			if($spdetail_origin ne '') {
				print $cgi->p("$spdetail_origin ");
			}
			#if growth_habit, printout
			if($spdetail_growth_habit ne '') {
				print $cgi->p("$spdetail_growth_habit");
			}
			
			#if blooming_dt , printout
			if($spdetail_blooming_dt ne '') {
				print $cgi->p("$spdetail_blooming_dt ");
			}
		#otherwise printout the exact $spdetail_Status, we shouldn't 
		#get too much of these output:
		}else{
			print $cgi->p("$spdetail_Status");
		}				

	}

print <<"TABLETHREE";
				</TD>
			</TR>
			<TR>
				<TD colspan=1 align="center">
TABLETHREE

	print $cgi->a({-href=>"/cgi-bin/searchspecimen.cgi?SpCode=".$cgi->escape($spdetail_Taxcd)."&Genus=".$cgi->escape($spdetail_genus)."&Family=".$cgi->escape($spdetail_FAMILY)."&Species=".$cgi->escape($spdetail_species)."&Common=".$cgi->escape($spdetail_common)}, "View Herbarium Records");










print <<"TABLEFOUR";
				</TD>
			</TR>
		</TABLE>
			</TD>
		</TR>
		<TR>
			<TD Align="Left"> <BR>


TABLEFOUR








	}else{
		if($synonym_printed == 1){
			#we've already printed the "Synonyms:" heading
			;
		}else{
			#otherwise we have some synonyms, but 
			# we've not printed the heading yet, so do so:
			print("<br><b>Synonyms</b>");
			print("<ul>");
			$synonym_printed = 1;
		}
		print("<li>");
		my $tax = getTaxonNm($spdetail_Taxcd, $spdetail_Syncd);
		print("$tax");
		print("</li>");
	}
#END spdetail record loop
}
print("</ul>");









print <<"TABLEFIVE";
                                </TD>
                        </TR>
                        <TR>
                                <TD Align="Left">
				&nbsp;


TABLEFIVE











 	while(my ($Taxcd, $Descp, $habitat_id) = $sththree->fetchrow_array()) {
		if($first_loop_flag_two == 0){
			$first_loop_flag_two = 1;
			print("<br><b>Habitat</b>  - Based on data collected by John T. Curtis (<a href=\"/herb/wwwherbarium/wisflora/bibliography.asp\">1959</a>) as compiled by C.E. Umbanhowar, Jr.");
			print("<ul>");
                        print("<li>");
                        print("<a href=\"/herb/wwwherbarium/wisflora/curtis.asp#$Descp\">$Descp</a>");                        print("</li>");

		}else{
			print("<li>");
			print("<a href=\"/herb/wwwherbarium/wisflora/curtis.asp#$Descp\">$Descp</a>");
			print("</li>");
		}
	}
	print("</ul>");






print <<"TABLESIX";
                                </TD>
                        </TR>
                        <TR>
                                <TD>&nbsp;
TABLESIX







	print("<br><b>More Information</b><br>");
	if(($dot_exists == 1 || $hand_exists == 1) && $first_loop_flag_three == 0 ) {
		$first_loop_flag_three = 1;
		print("<BR>");
		print("Distribution Maps");
		print("<ul>");
	}
	if($dot_exists == 1) {
		print("<li>$dot_url</li>");
	}elsif($hand_exists == 1) {
		print("<li>$hand_url</li>");
	}else{ 
		print("<br>No distribution maps found<br>");
	}
	print("</ul>");
	if($usda_exists == 1) {
		print("<ul>");
		print("<li>$usda_url</li>");
		print("</ul>");
	}
	print("Other Maps");
	print("<ul>");
	print("<li><a href=\"/herb/wwwherbarium/wisflora/ReferenceMaps.asp\">Wisconsin Reference Maps: Geology, Vegetation, Climate, Soils, etc.</a></li>");
	print("<li><a href=\"/herb/wwwherbarium/wisflora/images/WISCounties.gif\">Map with Wisconsin County Names</a></li>");
	print("</ul>");

















	# here we loop through our recently built array of information concerning the non-photo link table records for this species:
	print("<ul>");
	foreach(@nonphotos){
		print("<li>");
		print;
		print("</li>");
	}
	print("</ul>");
	print("<ul>");
	print("<li><a href=\"http://www.google.com/search?&q=$Genus $Species\">Search Google</a><ul><li>Find more information about $Genus $Species</li></ul></li>");
#the google url for "Bidens comosus" image search looked like this:
#http://images.google.com/images?q=Bidens+comosus&um=1&ie=UTF-8&sa=N&tab=wi
#ours is close to that:
	print("<li><a href=\"http://images.google.com/images?q=$Genus $Species\">Search Google Images</a><ul><li>Find more images of $Genus $Species</li></ul></li>");
	print("</ul>");






print <<"TABLESEVEN";
                                </TD>
                        </TR>
                </TABLE>
                </td>
		 <td width="40%" valign="top">
                <TABLE width="100%" height="100%" border=0>
                        <TR>
                                <TD align="center">
TABLESEVEN





#________________________________________________________________________________
# PHOTOS from spdetail:
#________________________________________________________________________________
	if($Photo ne "") {
		$Photo=~s/\.\.\/photos/\/herb\/wwwherbarium\/wisflora\/pictures\/xl_photos\//g;
		my $MainPhoto = $Photo;
		$MainPhoto=~s/xl_photos/mainphoto/g;
		$Photo=~s/\.jpg$/_XL.jpg/g;
		if(-e $Photo){
			print("<a href=\"$Photo\"><img src=\"$MainPhoto\"></a>");
			print("<a href=\"$Photo\">View Large Image</a>");
		}else{
			print("<img src=\"$MainPhoto\">");
		}
	}
	if($Photographer ne "") {
		print("<br>Photographer: ");
		print(" <a href=\"/herb/wwwherbarium/wisflora/photographers.asp\"> $Photographer </a><br>");
	}
#________________________________________________________________________________
# PHOTOS FROM link...
#________________________________________________________________________________
	#length_of_photos holds the length of the @photos array:
	my $length_of_photos = @photos;
	my $i;
	if($length_of_photos > 0) {
		print("<br>More Photos<br>\n");
		# loop through the @photos array to construct the web page's "More photos" section
		for($i=0, $i<$length_of_photos, $i) {
		##ERROR: perhaps we need to do $i<$length_of_photos, because I see errors like:
		# uninitialized value 439 461 462 in subsititutions/// and comparison ne
			#print("<BR>i $i<br>");
			#@photos is an array with sets of three values....like this:
			#link:Link, link:Title, link:Description, 
			#if the Title part is blank:
			if($photos[$i+1] ne ""){
				my $L = $photos[$i];
				my $T = $photos[$i+1];
				my $D = $photos[$i+2];
				my $Thumb = $T;
				$Thumb=~s/\.\.\//\/herb\/wwwherbarium\/wisflora\/pictures\//g;
				#$L=~s/\.\.\/bigphoto/\/herb/wwwherbarium\/wisflora\/pictures\/xl_photos\//g;
				$L=~s/\.\.\/bigphoto/\/herb\/wwwherbarium\/wisflora\/pictures\/photo\//g;
				print("<a href=\"$L\"><img src=\"$Thumb\"></a><br>\n");
				print("<a href=\"$L\">View Image</a><br>\n");
				$L=~s/photo/xl_photos/g;
				$L=~s/\.jpg$/_XL.jpg/g;
				my $path = "/var/www/html/".$L;
				#print("<BR>path $path<br>");
				if(-e $path){
					print("<a href=\"$L\">View Large Image</a><br>\n");
				}
			#otherwise if the link:Title is blank:
			}else{
				my $L = $photos[$i];
				my $T = $photos[$i+1];
				#I get uninitialized value errors here:
				my $D = $photos[$i+2];
				$L=~s/\.\.\/bigphoto/\/herb\/wwwherbarium\/wisflora\/pictures\/photo\//g;
				#for some reason, $L is occasionally empty...check on that!
				if(length($L) > 1) {
					print("<a href=\"$L\"><img src=\"$L\"></a><br>\n");
print<<"TABLESEVENTWO";
						</TD><TD align="center">
TABLESEVENTWO
				}
			}
			#this should be okay because this query against the link table:
			# SELECT * FROM link WHERE Description = "";
			# 0 records (empty set)
			# and so $photos[$i+2] should never have an empty field:
			#I get uninitialized value errors here:
			# and so test first:
			if(length($photos[$i+2]) > 1){
				print("<a href=\"/herb/wwwherbarium/wisflora/photographers.asp\"> $photos[$i+2] </a><br><br><br>");
			}
			$i+=3;
		# end for loop
		}
	#end if($length_of_photos > 0)
	}else{ 
		print("<p>No additional photos for this taxon</p>");
		print("<a href=\"/RequestPhoto.html\">No photograph available -<br> We request that you submit a photo</a>");
	}
	$dirname = "/var/www/html/thumbs/";
	$bigdirname = "/var/www/html/bigpic/";
	opendir(DIR,$dirname);
	while(defined($file = readdir(DIR))) {
		if($file=~/$SpCodeParam/) {
			print("<a href=\"/bigpic/$file\"><img src=\"/thumbs/$file\"</a>");
		}
	}
	print("<br><a href=\"/uploadpic/photoRequest.php?SpCode=$SpCodeParam\">User submitted photos</a>");
	

print <<"TABLEEIGHT";

                                </TD>
                        </TR>
                </TABLE>
                <TABLE border=0 align='center' valign='top'>
                        <tr>
                                <td>&nbsp;

TABLEEIGHT









# GET AND PRINT specimen scans :
#Loop through records from this SQL:"SELECT ACCESSION, TYPE FROM specimen WHERE Taxcd = '$SpCodeParam' AND scan = '1'"
	while(my ($ACCESSION, $TYPE) = $sthfour->fetchrow_array()) {
		if($TYPE ne "") {
			my $baseurl = "/herb/wwwherbarium/wisflora/pictures/specimenscans";
			my $thumburl = "$baseurl/200px/$ACCESSION"."_thumb.jpg";
			my $smallurl = "$baseurl/500px/$ACCESSION"."_medium.jpg";
			my $mediumurl = "$baseurl/800px/$ACCESSION"."_large.jpg";
			my $largeurl = "$baseurl/full size/$ACCESSION".".jpg";
			print("<BR><BR>Specimen Scan<BR>");
			
			print("<br><a href=\"$smallurl\"><img src=\"$thumburl\"></a>");
			print("<br><a href=\"$mediumurl\">View Large Image</a>");
			print("<br><a href=\"$largeurl\">View X-Large Image</a>");
			print("<br><a href=\"/cgi-bin/specimen.cgi\">View Specimen scan details</a>");
		}else{ 
			print("<br>No specimen scans for this taxon<br>");
			#print("<br>$ACCESSION<BR>$TYPE<br>");
		}
	}




print <<"TABLENINE";

                                </td>
                        </tr>
                </TABLE>
                </td>
        </tr>
</TABLE>
TABLENINE

print <<"FOOTER";
<br>
<table width="100%" border="0">
  <tr bgcolor="#EEEEEE">
    <td align="center" width="25%">
      <p><strong>Menu:</strong> <font size=2><a href="/herbarium/"><b>Herbarium Home</b></a></font> </p></td>
    <td align="center" width="25%"> <font size="2"><a href="/wisflora/"><b>WISFLORA: Vascular Plant Species</b></a></font></td>
    <td align="center" width="25%"> <font size="2"><a href="/herb/search.html"><b>Vascular Plant Taxon Search</b></a></font> </td>
    <td align="center" width="25%"> <font size="2"><a href="/herb/specimenSearch.html"><b>Search Specimen Database</b></a></font> </td>
  </tr>
</table>
FOOTER





} # end scope
$dbh->disconnect ();
print $cgi->end_html();
exit (0);
sub getTaxonNm
{
	my ($taxcd, $syncd) = @_;
	my $taxonName = "";
	#we already have a db connection setup...so make a statement handle:
	my $sth = $dbh->prepare ("SELECT * FROM spdetail WHERE Taxcd = '$taxcd' AND Syncd = '$syncd' ORDER BY FAMILY, Taxcd, Syncd");
	$sth->execute();
 	while (my ($Taxcd, $Syncd, $family_code, $genus, $species, $authority, $subsp, $variety, $forma, $subsp_auth, $var_auth, $forma_auth, $sub_family, $tribe, $common, $Wisc_found, $ssp, $var, $f, $hybrids, $status_code, $hide, $USDA, $COFC, $WETINDICAT, $FAM_NAME, $FAMILY, $GC, $FAMILY_COMMON, $SYNWisc_found, $SYNS_STATUS, $SYNV_STATUS, $SYNF_STATUS, $SYNHYBRIDS_STATUS, $SYNW_STATUS, $speciesweb_Taxcd, $Status, $Photo, $Photographer, $Thumbmaps, $Accgenus, $SORTOR, $Hand, $growth_habit_bck, $blooming_dt_bck, $origin_bck, $Thumbphoto, $date_time, $growth_habit, $blooming_dt, $origin, $Taxa, $spdetail_id ) = $sth->fetchrow_array ()){
		#Here is the base name construction:
		$taxonName = $genus." ".$species." ".$authority;
		# $strcd will hold either the current record's $taxcd or the $syncd
		my $strcd = "";
		#if the syncd is ".", set $strcd to the $taxcd value:
		if($syncd eq "."){
			$strcd = $taxcd;
		#otherwise, the syncd is not ".", so set $strcd to the $syncd value:
		}else{
			$strcd = $syncd;
		}
		#does it have forma:
		if($strcd=~/f/){
			#my $f = $forma;
			$taxonName .= " f. ".$forma." ".$forma_auth;
		}
		if($strcd=~/v/){
			#there is also $var
			#my $v = $variety;
			$taxonName .= " var. ".$variety." ".$var_auth;
		}
		if($strcd=~/x/){
			#there is also a $Status (and other statuses??)
			#my $x = $status_code;
			#not sure why we repeat forma concatenation...apparently if there is a forma, then it won't we EXCLUDED and vice-versa???:
			$taxonName .= " X ".$forma." ".$forma_auth;
		}
		if($strcd=~/s/){
			#there is also $ssp
			#my $s = $subsp;
			$taxonName .= " subsp. ".$subsp;
		}
	}
	return($taxonName);
}
__DATA__
