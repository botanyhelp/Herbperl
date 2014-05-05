#!/usr/bin/perl
# lichenSearchResults.cgi -wislichens Results page for species searching
use strict;
use warnings;
use CGI;
use DBI;
use URI::URL;
use Data::Dumper;
my $title = "lichenSearchResults.cgi";
my $cgi = new CGI();
print $cgi->header(); 
print $cgi->start_html(-title => $title, -bgcolor => "white");
print <<HERBHEADER;
<table width="100%" border="0" bgcolor="#EEEEEE">
  <tr bgcolor="#E7E7B6">
    <td width="100%" bgcolor="#E7E7B6"><font color="#990000"><font size=+3>W
</font><b><font size=+1>ISCONSIN </font></b><font size=+3>B</font><b><font 
size=+1>OTANICAL </font></b><font size=+3>I</font><b><font size=+1>NFORMATION 
</font></b><font size=+3>S</font><b><font size=+1>YSTEM</font></b></font></td>
  </tr>
  <tr>
    <td><table width="100%" border=0>
        <tr>
          <td width="400%" colspan="4" bgcolor="#A9BB97">
            <table width="100%">
              <tr>
                <td width="30%"> <b><i><font color="#990000" size="4">Wisconsin
 State Herbarium</font></i></b> </td>
                <td width="40%" align="center" VALIGN="middle">
                <p><font size="4"><b>Wisflora - Vascular Plant Species</b>
</font></p></td>
                <td VALIGN="CENTER" width="30%">
                  <div align="right"> <b><font size="-1">University of&nbsp; 
Wisconsin - Madison&nbsp;</font></b> </div></td>
              </tr>
          </table></td>
        </tr>
    </table></td>
  </tr>
</table>

<table width="100%" border="0">
  <tr bgcolor="#EEEEEE">
    <td align="center" width="25%">
      <p><strong>Menu:</strong> <font size=2><a href="/wislichens/"><b>Lichen 
 Home</b></a></font> </p></td>
    <td align="center" width="25%"> <font size="2"><a href="/wislichens/"><b>
</b></a></font></td>
    <td align="center" width="25%"> <font size="2"><a href="/wislichens/">
<b></b></a></font> </td>
    <td align="center" width="25%"> <font size="2"><a 
href="/wislichens/"><b></b></a></font> 
</td>
  </tr>
</table>
HERBHEADER

my $dsn = "DBI:mysql:host=localhost;database=lichenten";
my $dbh = DBI->connect($dsn, "apache", "apachePASS") or die "cantconnect $!";
my $familyParam = "";
my $genusParam = "";
my $speciesParam = "";
my $commonParam = "";
my $habitatParam = "";
my $statusParam = "";
my $countyParam = "";
my $status1Param = "";
my $nativeParam = "";
#lastFamily and lastGenus hold the values from the last record to prevent 
#repeated printing
my $lastFamily= "";
my $lastGenus = "";
#prevTaxcd is used to determin if the lst taxcd
my $prevTaxcd = "notthis";
if($familyParam = $cgi->param("Family")){
	#append a SQL-wildcard % onto the parameter
#	print $cgi->p("fam");
	$familyParam .= '%';
}else{
	$familyParam= "";
}
if($genusParam = $cgi->param("Genus")){
	#append a SQL-wildcard % onto the parameter
#	print $cgi->p("gen");
	$genusParam .= '%';
}else{
	$genusParam= "";
}

if($speciesParam = $cgi->param("Species")){
	#append a SQL-wildcard % onto the parameter
#	print $cgi->p("gen");
	$speciesParam .= '%';
}else{
	$speciesParam= "";
}

if($commonParam = $cgi->param("Common")){
	#prepend and append a SQL-wildcard % onto the parameter
#	print $cgi->p("spe");
	#remove single-quotes...so that the SQL statement does't get 
	# mismatched on common names with apostrophes, like "adam's-needle"
	$commonParam=~s/'/\\'/g;
	$commonParam = '%'.$commonParam.'%';
}else{
	$commonParam = "";
}
if($habitatParam = $cgi->param("Habitat")){
        $habitatParam .= '%';
}else{
        $habitatParam= "";
}
if($statusParam = $cgi->param("Status")){
        $statusParam .= '%';
        #$statusParam = '%'.$statusParam;
}else{
        $statusParam= "";
}
if($countyParam = $cgi->param("County")){
        $countyParam .= '%';
}else{
        $countyParam= "";
}
#notice that nativeParam holds the value of parameter named "Native", 
# but that the column in spdetail we compare to is called "origin"
if($nativeParam = $cgi->param("Native")){
        $nativeParam .= '%';
}else{
        $nativeParam= "";
}
#notice that status1 is not status...even though both refer to the same 
# "Status" field in spdetail...statusParam comes from the statussearch.html
# page and status1Param comes from countysearch.html:
if($status1Param = $cgi->param("Status1")){
        $status1Param.= '%';
}else{
        $status1Param= "";
}







{ # begin scope
	#MUCH FASTER 0.
	my $sqlone = "";
	if($habitatParam eq "" and $countyParam eq "") {
		$sqlone = "SELECT DISTINCT Taxcd FROM spdetail WHERE ";
		#$appendAND is a flag used to let us know whether we 
		# need to add and "AND" to our query or not:
		my $appendAND = 0;
		if($familyParam ne ""){
			#$sqlone .= "hide != 'Y' AND family LIKE '$familyParam'";
			$sqlone .= "family LIKE '$familyParam'";
			$appendAND = 1;
		}
		if($genusParam ne ""){
			if($appendAND == 0){
				#$sqlone .= "hide != 'Y' AND genus LIKE '$genusParam'";
				$sqlone .= "genus LIKE '$genusParam'";
			}else{
				$sqlone .= " AND genus LIKE '$genusParam'";
			}
			$appendAND = 1;
		}
		if($speciesParam ne ""){
			if($appendAND == 0){
				#$sqlone .= "hide != 'Y' AND species LIKE '$speciesParam'";
				$sqlone .= "species LIKE '$speciesParam'";
			}else{
				$sqlone .= " AND species LIKE '$speciesParam'";
			}
			$appendAND = 1;
		}
		if($commonParam ne ""){
			if($appendAND == 0){
				#$sqlone .= "hide != 'Y' AND common LIKE '$commonParam'";
				$sqlone .= "common LIKE '$commonParam'";
			}else{
				$sqlone .= " AND common LIKE '$commonParam'";
			}
			$appendAND = 1;
		}
	        if($statusParam ne ""){
			my $oldStatusParam = $statusParam;
			if($statusParam=~/Ecologic/){
				#this matches invasive species better:
				$statusParam = "%nvasiv%";
			}
			if($appendAND == 0){
	                	#$sqlone .= " Status LIKE '$statusParam'";
	                	$sqlone .= " Status1 LIKE '$statusParam'";
			}else{
				#$sqlone .= " AND Status LIKE '$statusParam'";
				$sqlone .= " AND Status1 LIKE '$statusParam'";
			}
			$statusParam = $oldStatusParam ;
	        }
	}elsif($countyParam ne ""){
		#this county searching is odd...it queries the "specimen" 
		# table to find records with a county like the one the user 
		# searched for.  This is slightly decieving, as some users 
		# surely think they are searching for plants found in that 
		# county, when in fact they are searching for specimen records 
		# that have "county" values equal to the one the user selected:
		$sqlone = "SELECT DISTINCT Taxcd FROM specimen WHERE county 
LIKE '$countyParam'";
	}elsif($habitatParam ne ""){
		#there has been a request for habitat type, which 
		# requires us to refer to a whole other table, habitat:
		# Do notice that this means that all habitat searching 
		# should occur independently, which is dumb.  
		$sqlone = "SELECT DISTINCT Taxcd FROM habitat WHERE Descp 
LIKE '$habitatParam'";
	}else{
		print("NEVER GET TO HERE!");
	}

	my $sthone = $dbh->prepare ($sqlone);
	$sthone->execute();
	#query_taxcd is an array that will hold the taxcd's we want records for
	my @query_taxcd = ();
	while (my ($taxcd) = $sthone->fetchrow_array ()){
		push(@query_taxcd, $taxcd);
	}
	
	#my $sqltwo = "SELECT taxcd, syncd, genus, family, species, common, 
#status_code, photo, thumbmaps, hand, Wisc_found FROM spdetail WHERE Taxcd IN (";
	my $sqltwo = "SELECT taxcd, syncd, genus, species, common, taxa, 
growthform, photobiont, abundance, status, photo, photographer, thumbmaps, 
Gallery, Sortor, Wisc_Found FROM spdetail WHERE Taxcd IN (";
	#loop through our query_taxcd list of taxcd values under consideration 
	# for the construction of our sql statement:
	foreach(@query_taxcd){
		#this adds a double-quote, current element of array, another 
		# double-quote, a comma and a space:
		$sqltwo .= "\"$_\", ";
	}
	#remove trailing space
	chop($sqltwo);
	#remove trailing comma
	chop($sqltwo);
	$sqltwo .= ") ";
	#if its a county search, add more logic to consider "status" and 
	# "origin" fields of records to be returned...this logic follows 
	# the County-web-page-form logic, which allows user to specify the status 
	# and origin in addition to the mandatory "County" search.  Because 
	# there are no other forms (yet that I know of) which allow one to 
	# do more mix-and-matching of search criteria, this code is sufficient 
	# for now.  However, if one were to create a web-page-form that 
	# allowed one to search for specific origin and status (without any 
	# county-specified criterion), then this code would need to be 
	# adjusted significantly.  NOTE: That query criteria I just mentioned,
	# is a very reasonable question for one to ask of our DB.  
	if($countyParam ne "") {
		if($nativeParam ne "") {
			$sqltwo .= " AND origin LIKE '$nativeParam' ";
		}
		if($status1Param ne "") {
			$sqltwo .= " AND Status LIKE '$status1Param' ";
		}
	}
	#$sqltwo .= " ORDER BY family, taxcd, syncd";
	$sqltwo .= " ORDER BY taxcd, syncd";
	my $sthtwo = $dbh->prepare ($sqltwo);
	
	#If a genusParam was passed, use that instead to prepare our SQL statement:
	$sthtwo->execute();
	my $families;
	#initialize control variables used to recall whether we've already 
	# seen fam,gen,tax:
	my %seenf = ( "FAMBABY" => 1);
	my %seeng = ( "GENBABY" => 1);
	my %seent = ( "SPEBABY" => 1);
	#this should be renamed to hash_of_asn or hash_of_canonicalNames:
	my %hash_of_taxcd;
	#this should be renamed to hash_of_synonyms or hash_of_nonCanonicalNames:
	my %hash_of_common;

#FTHRE:	while (my ($taxcd, $syncd, $genus, $family, $species, $common, 
#$status_code, $photo, $thumbmaps, $hand, $Wisc_found) = 
#$sthtwo->fetchrow_array ()){
#	my $sqltwo = "SELECT taxcd, syncd, genus, species, common, taxa, 
#growthform, photobiont, abundance, status1, photo, photographer, thumbmaps, 
#Gallery, Sortorder, Wisc_Found FROM spdetail WHERE Taxcd IN (";
FTHRE:	while (my ($taxcd, $syncd, $genus, $species, $common, $taxa,
$growthform, $photobiont, $abundance, $status_code, $photo, $photographer, 
$thumbmaps, $Gallery, $Sortorder, $Wisc_found) = 
$sthtwo->fetchrow_array ()){
		my $family = "lichenFamily";
		my $hand = "handPASS";
		if($taxcd eq $prevTaxcd) {
			#print("This taxcd should be skipped because its not in WI:<BR>");
			#print("$taxcd, $syncd, $genus, $family, $species, 
			# $common, $status_code, $photo, $thumbmaps, $hand, 
			# $Wisc_found");
			#print("<br>");
			#Yes, this should be skipped because its taxon has already been handled
			# based on the fact that the "order by" clause in the SQL statement 
			# above causes the taxon with syncd="." to come out first (recall that 
			# many records with same taxon field value can come out, and so they 
			# in turn are sorted by syncd, which means that (based on the next if 
			# clause below) the "canonical" (i.e. syncd=.) record was already 
			# examined on the previous fetchrow_array() execution.  And so anytime 
			# that ($taxcd eq $prevTaxcd) is true, we should skip:
			next FTHRE;
		}
		if($syncd eq "." and $Wisc_found ne "W"){
			#save current taxon:
			$prevTaxcd = $taxcd;
			#but if we are not canonical and not in wisconsin, move on.
			# notice that to get here, we also know that the current 
			# record under consideration has a taxon code not equal to 
			# the taxon code of the previous record.  This "coupling"
			# between the program logic and the order-of-records-returned
			# should be removed with a better program design.  In any 
			# case, this code logic works because all records not found 
			# in Wisconsin are tossed and not considered:
			next FTHRE;
		}
		#here we collect ALL the data:
		#if the record is an ASN, keep it in our keyed-by-taxcd hash 
		# for later printout:
		if($syncd eq '.' and $Wisc_found eq 'W'){
			#add this record to the growing hash of ASNs. There is one ASN per
			# taxon code.  This hash should be named hash_of_ASNs:
			$hash_of_taxcd{$taxcd} = [$taxcd, $species, $syncd, 
$genus, $family, $species, $common, $status_code, $photo, $thumbmaps, $hand, 
$Wisc_found];
		#else, if its got a non-'.'  syncd value, its a synonym, and 
		# so collect it:
		}else{
			#push this record onto the growing list of synonyms associated with this
			# taxon code.  This hash should be named hash_of_synonyms:
			push(@{$hash_of_common{$taxcd}}, [$taxcd, $species, 
$syncd, $genus, $family, $species, $common, $status_code, $photo, $thumbmaps, 
$hand, $Wisc_found]);
		}
		#Now we begin a completely different stage of the program where we will 
		# build a data structure like this:
		# $families->{$family}->{$genus}->{$taxcd}->[[ASN],[SYN1],[SYN2],[SYN3]]
		# in memory, by filling the data structure with the data it gathers from 
		# the records being returned by the query resultset.  Note that the query 
		# resultset is not ideal and comes out with complete record information 
		# for a given taxon code, one record at a time.  By examining each record,
		# one at a time, we can build the data structure above, which is called a 
		# hash of hashes of hashes of hashes of arrays of arrays, or rather 
		# a hash keyed on family name strings holding hashes keyed on genus name 
		# strings holding hashes keyed on taxcd each holding an array of arrays, 
		# each of which is a simple list of miscellaneous data about the specific 
		# record (bearing the current taxcd) under examination.  
		#And so what follows is a bunch of control statements that try to build 
		# the data structure described above from the results of the query.  
		#if we've not yet seen the family, genus or taxcd, 
		if( !exists($seenf{$family}) and !exists($seeng{$genus}) and 
!exists($seent{$taxcd})) {
			#but first record the fact that we've seen this family, genus and taxcd:
			$seenf{$family} = 1;
			$seeng{$genus} = 1;
			$seent{$taxcd} = 1;
			#then add a data structure 
			# to the growing families hashref:
			$families->{$family} = {$genus => {$taxcd =>  
[[$species, $syncd, $common, $status_code, $photo, $thumbmaps, $hand, 
$Wisc_found]]}};
		#otherwise if we've seen the taxcd and the genus but not the family, 
		}elsif($seent{$taxcd} == 1 and !exists($seenf{$family}) and 
$seeng{$genus} == 1){
			#record that we've seen family:
			$seenf{$family} = 1;
			#then that is weird
			#print("This record is strange because we've already 
			# seen this taxcd and genus but not its family..HMM<BR>");
			#but nonetheless, we should just add it to our data structure:
			#since this record has a genus and taxcd we've seen, but not its 
			# family, we are free to make an entire family-level data structure 
			# and add it to the rest of our families:
			$families->{$family} = {$genus => {$taxcd =>  
[[$species, $syncd, $common, $status_code, $photo, $thumbmaps, $hand, 
$Wisc_found]]}};
		#otherwise if we've seen the taxcd but not the family or the genus,
		}elsif($seent{$taxcd} == 1 and !exists($seenf{$family}) and 
!exists($seeng{$genus})) {
			#record that we've now seen the family and the genus:
			$seeng{$genus} = 1;
			$seenf{$family} = 1;
			# then something weird is going on, namely, I think, that we are 
			# dealing with a record whose taxcd value indicates it is a synonym 
			# of a previously seen record but its family and genus values are 
			# different, that is, it is a synonym of a previously seen record 
			# but is currently in a different family and genus altogether:
			#print("This record is strange because we've already 
			# seen this taxcd, but not its family or its genus...HMM<BR>");
			#nonetheless we should add the data to our data structure.  Since 
			# we don't have any information about hte family or the genus, we'll 
			# need to make a all new  stuff, like when it is when we've never 
			# seen the family, genus or taxcd:
			$families->{$family} = {$genus => {$taxcd =>  
[[$species, $syncd, $common, $status_code, $photo, $thumbmaps, $hand, 
$Wisc_found]]}};
		#otherwise, check if we've not seen this genus before, 
		# but have seen the family before:
		}elsif($seenf{$family} == 1 and !exists($seeng{$genus}) ){
			#record that we've seen the genus and taxcd:
			$seeng{$genus} = 1;
			$seent{$taxcd} = 1;
			#so create another data structure for this genus:
			$families->{$family}->{$genus} = {$taxcd =>  
[[$species, $syncd, $common, $status_code, $photo, $thumbmaps, $hand, 
$Wisc_found]]};
		#otherwise, check if we've seen both this genus and family 
		# but not taxcd before:
		}elsif($seeng{$genus} == 1 and $seenf{$family} == 1 and 
!exists($seent{$taxcd}) ){
			#record that we've seen taxcd
			$seent{$taxcd} = 1;
			#we've already seen this family and genus, but not the taxcd, 
			# so add a taxcd record as the first element of a new 
			# arrayref-of-arrayrefs.  
			$families->{$family}->{$genus}->{$taxcd} =  
[[$species, $syncd, $common, $status_code, $photo, $thumbmaps, $hand, 
$Wisc_found]];
		#otherwise, we've seen this family, genus and taxcd before:
		}elsif($seeng{$genus} == 1 and $seenf{$family} == 1 and 
$seent{$taxcd} == 1 ){
			#and so we want to push onto its taxcd record another anonymous 
			# arrayref with the rest of the data for this record.
			push(@{$families->{$family}->{$genus}->{$taxcd}}, 
[$species, $syncd, $common, $status_code, $photo, $thumbmaps, $hand, 
$Wisc_found]);
		}else{
			print("SHOULD NEVER GET HERE<BR>");
			print("$family<BR>$genus<BR>$taxcd<BR>$species<BR>");
		}
	}
	if((scalar (keys %hash_of_taxcd)) == 0) { 
		print("No records matched your query<BR>");
	}
	
		#end while loop
	#print a dump of the data structure we've created,
	# which makes it easy to visualize the data in a 
	# hash of hashrefs of hashrefs of arrayrefs of arrayrefs
	#...be sure to use the HTML <PRE> tag to keep all the 
	# nice whitespace produced by Data::Dumper:
	#print("<PRE>");
	#print Dumper($families);
	#print("</PRE>");

	#declare some variables used as we walk through the data structure to
	# pull out the right data at the right time.  
	my $fam;
	my $gen;
	# taxon code
	my $t;
	#here we run through the families, in alphabetical order, followed 
	# by the genera, also in alphabetical order, followed by the taxcds,
 	# in alphabetical order.  On the way to all-the-data at the bottom 
	# of this data structure, we test to see if we should printout the 
	# name of the family under consideration (YES, if we've not done so 
	# yet!), and if we should printout the genus (Yes, if nyet).  For 
	# each genus we consider, we see first if it contains any canonical 
	# records, and if so, printout the word "Genus: Aster".  Then for 
	# each taxon record in that genus we printout the ASN information 
	# followed by the synonyms we stored in hash_of_common.  Then we skip to 
	# the next genus in the foreach output.  
	#One existing problem is that 
	# if someone searches on a genus then the records that get returned 
	# may be from other genera.  That is there may be records where the 
	# current genus name is different from the genus name we asked for.  
	# This would happen when a record is a synonym for an ASN that exists 
	# in a different genera.  For example, asking for genus=solidago records 
	# returns some records that are currently in the "Aster" genus.  These 
	# records should be in the output, since they are synonyms of species 
	# that are in the genus "Aster".  However, if we ask for genus=Solidago 
	# then our records will contain results that are stored under the genus 
	# of Aster, and, as a result, will be printed out, and since we printout 
	# in alphabetical order, we get the "wrong" (according to Galen) order 
	# for herbarium users.  To correct this problem the algorithm might be:
	# ===============================================
	# 1. determine if a genus was specified, by seeing if $genusParam ne ""
	# 2. if so, switch logic to printout that genus first, no matter what.  
	# 3. the logic switch could work such that:
	#		if(exists({$families->{$fam}->{chop($genusParam)}
	#    then use that record first! (the chop chops off the extra % 
	# appended for sql)
	# 4. 
	# ===============================================
	#test if habitatParam is set, if so, print out habitat blurb
	if($habitatParam ne ""){
		#chop off trailing "%" percent symbol 
		chop($habitatParam);
		#according to the old scripts, we are supposed to 
		# use hablink table to look up links/Titles for 
		# this habitat.  Hmmm...
		print("<h2>Habitat type: $habitatParam</h2>");
	}
	#test if $countyParam is set:
	if($countyParam ne ""){
		#chop off trailing "%" percent symbol 
		chop($countyParam);
		print("<h2>County: $countyParam</h2>");
	}
	#test if $nativeParam is set:
	if($nativeParam ne ""){
		#chop off trailing "%" percent symbol 
		chop($nativeParam);
		print("<h2>Origin: $nativeParam</h2>");
	}
	#test if statusParam is set, if so, print out status blurb
	if($statusParam ne ""){
		#chop off trailing "%" percent symbol 
		chop($statusParam);
		print("<h2>Status: $statusParam</h2>");
		print("<A HREF=\"/composition.asp#$statusParam\">Definition</A>");
                print("<A HREF=\"http://www.dnr.state.wi.us/org/land/er/biodiversity.htm\">
		Wisconsin DNR Status Information</A>");

	}

	# $genusFirst is a flag 
	my $genusFirst = 0;
	# for each family in the data structure
        foreach $fam (sort keys %$families){
                print("<br><FONT SIZE=+2>Family: $fam</FONT>"); 
		#if the user specified a genus, and that genus exists in our
		# data structure: (perhaps also add a test to see if it was the first 
		# to be output in the sorted-by-key hash anyway, as genus=Aster usually
		# would, for example).
		#if($genusParam=~/%/ and exists($families->{$fam}->{chop($genusParam)})) {
		chop($genusParam); 
		#print("$genusParam<BR><BR>");
		if(exists($families->{$fam}->{$genusParam}) and $genusFirst == 0) {
			#print("<BR><BR>OK<BR><BR>");
			#then lets make sure it is the first  
			# to do so, we put out that genus first, and then just skip 
			# it later on when all of the genera are examined.  
			if(Dumper($families->{$fam}->{$genusParam})=~/'\.',/ ){
		               	print $cgi->b("<br>&nbsp;&nbsp;Genus: $genusParam"); 
			}
			foreach $t (sort keys %{$families->{$fam}->{$genusParam}} ){
				if(Dumper($families->{$fam}->{$genusParam}->{$t})=~/'\.',/ ){
					print("<br>&nbsp;&nbsp;&nbsp;&nbsp;");
					print $cgi->a({-href=>"/cgi-bin/lichendetail.cgi?SpCode=".
$cgi->escape(@{$hash_of_taxcd{$t}}[0])."&Genus=".(@{$hash_of_taxcd{$t}}[3])."&Family=".
$cgi->escape(@{$hash_of_taxcd{$t}}[4])."&Species=".
$cgi->escape(@{$hash_of_taxcd{$t}}[1])."&Common=".
$cgi->escape(@{$hash_of_taxcd{$t}}[6])."&photo=".
$cgi->escape(@{$hash_of_taxcd{$t}}[8])."&thumbmaps=".
$cgi->escape(@{$hash_of_taxcd{$t}}[9])."&hand=".
$cgi->escape(@{$hash_of_taxcd{$t}}[10])}, 
getTaxonNm(@{$hash_of_taxcd{$t}}[0], @{$hash_of_taxcd{$t}}[2]));
					my $comm = 
$families->{$fam}->{$genusParam}->{$t}->[0]->[2];
					#printout * if photo:
					if(@{$hash_of_taxcd{$t}}[8]=~/jpg/i){
						print("*");
					}
					#printout  + if map:
					if(@{$hash_of_taxcd{$t}}[9]=~/gif/i){
						print("+");
						print("<BR>");
					}elsif(@{$hash_of_taxcd{$t}}[10]=~/H/i){
						print("+");
						print("<BR>");
					}
					print("<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;");
					print("$comm");
					my $s =  @{$hash_of_taxcd{$t}}[0];
					foreach(@{$hash_of_common{$s}}){
						print("<BR>&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;");
						print(getTaxonNm($$_[0], $$_[2]));
					}
				}
			}
			$genusFirst = 1;
		}
		#print("<BR><BR><BR>Other Genera<BR><BR><BR>");
		# for each genus in this family data structure:
GEN:            foreach $gen (sort keys %{$families->{$fam}}) {
			if($genusFirst == 1){ 
				#comparing the $gen to the $genusParam won't work 
				# because they have the same value even when their 
				# taxcd values differ greatly.  Therefore the right 
				# test here might be if the $gen value matches the 
				# first three digits of the taxcd.??? If so, then 
				# yes, skip it.  
				if($gen eq $genusParam){
		#			print("<BR><BR><BR>ALREADY SEEN<BR><BR><BR>");
					#if we get here it means that the user did 
					# specify a genus and that that genus has 
					# already been printed out, so skip it:
					next GEN;
				}
			}
			if(Dumper($families->{$fam}->{$gen})=~/'\.',/ ){
		               	print $cgi->b("<br>&nbsp;&nbsp;Genus: $gen"); 
			}
			#notice in the following foreach loop that we sort the 
			# keys returned...this is not required even though it causes 
			# the first key to be returned to be the $t with a value 
			# of "." and thus the ASN record.  This is not required, 
			# however, because we only want to printout the ASNs here 
			# and we'll use the taxcd of the ASN to lookup information 
			# about its synonyms.  The point is that even though the ASN 
			# is coming out as the first record we consider, this code 
			# logic does not require that and so the sort order can 
			# change if there is a better way than the current order with
			# is alphabetically by taxcd (perhaps not brilliant).  
			# for each taxon code in this genus data structure:
			foreach $t (sort keys %{$families->{$fam}->{$gen}} ){
				#Here we (crudely) use Data::Dumper module to dump 
				# the data structure looking for the sequence that 
				# indicates we are dealing with a taxon code with 
				# at least one (and, actually, only one) record 
				# with the syncd of '.' or period.  The Data::Dumper 
				# output has a four-char sequence '.', that we are 
				# searching for.  If we find it, then we'll have to 
				# generate some output because it means there is 
				# a good record under examination.
				#if the record is an ASN, print the link:
				if(Dumper($families->{$fam}->{$gen}->{$t})=~/'\.',/ ){
					print("<br>&nbsp;&nbsp;&nbsp;&nbsp;");
					#printout the link to the accepted species name ASN:
					print $cgi->a({-href=>"/cgi-bin/lichendetail.cgi?SpCode=".
$cgi->escape(@{$hash_of_taxcd{$t}}[0])."&Genus=".(@{$hash_of_taxcd{$t}}[3])."&Family=".
$cgi->escape(@{$hash_of_taxcd{$t}}[4])."&Species=".
$cgi->escape(@{$hash_of_taxcd{$t}}[1])."&Common=".
$cgi->escape(@{$hash_of_taxcd{$t}}[6])."&photo=".
$cgi->escape(@{$hash_of_taxcd{$t}}[8])."&thumbmaps=".
$cgi->escape(@{$hash_of_taxcd{$t}}[9])."&hand=".
$cgi->escape(@{$hash_of_taxcd{$t}}[10])}, getTaxonNm(@{$hash_of_taxcd{$t}}[0], 
@{$hash_of_taxcd{$t}}[2]));
					   #printout * if photo:
                                        if(@{$hash_of_taxcd{$t}}[8]=~/jpg/i){
                                                print("*");
                                        }
                                        #printout  + if map:
                                        if(@{$hash_of_taxcd{$t}}[9]=~/gif/i){
                                                print("+");
                                        }elsif(@{$hash_of_taxcd{$t}}[10]=~/H/i){
                                                print("+");
                                        }

					#since we are currently dealing with an ASN, its 
					# common field holds a bonafide common name that 
					# we should printout also:
					my $comm = $families->{$fam}->{$gen}->{$t}->[0]->[2];
					#if the common name is not blank, printout
					if(length($comm) > 1){
						print("<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;");
						print("$comm");
					}
					#here we want to use the $t taxon code string to find 
					# the first field of its arrayref value in hash_of_taxcd
					# that 1st
					# field is the record's  taxon code
					my $s =  @{$hash_of_taxcd{$t}}[0];
					#hash_of_common is a hash keyed on syncd  
					# whose value is a reference to 
					# an array of array-refs, 
					#Here we loop through hash_of_common's contents 
					# and call getTaxonNm once for each value in 
					# the hash_of_commons:
					# for each arrayref returned from hash_of_commons,
					foreach(@{$hash_of_common{$s}}){
						print("<BR>&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;");
						#these records represent synonyms of the taxcd
						# under consideration, and so for each synonym, 
						# we use the taxcd and syncd to print out 
						# the getTaxonNm result:
						print(getTaxonNm($$_[0], $$_[2]));
						#this is taxcd and space and syncd:
						#print($$_[0], " ", $$_[2]);
					#end the foreach hash_of_commons for this taxcd
					}
				#end the if where we see Dumper output contains "."
				}
			#end the "taxcd" foreach 
			}
			#We are about to hop out because we've examined
			# all of the taxon codes in that gener:
			#Notice that this  code is not too careful:
			#next GEN;
		#end foreach $gen
                }
	#end family foreach
        }
}
 # end scope
$dbh->disconnect ();
print <<HERBFOOTER;
<br>
<table width="100%" border="0">
  <tr bgcolor="#EEEEEE">
    <td align="center" width="25%">
      <p><strong>Menu:</strong> <font size=2><a href="/wislichens/"><b>Lichen Home 
</b></a></font> </p></td>
    <td align="center" width="25%"> <font size="2"><a href="/wislichens/"><b>
</b></a></font></td>
    <td align="center" width="25%"> <font size="2"><a href="/wislichens/">
<b></b></a></font> </td>
    <td align="center" width="25%"> <font size="2"><a href="/wislichens/">
<b></b></a></font> </td>
  </tr>
</table>
HERBFOOTER
print $cgi->end_html();
exit (0);




# _GET_TAXON_NAME getTaxonNmj
sub getTaxonNm
{
	my ($taxcd, $syncd) = @_;
	my $taxonName = "";
	my $dsntwo = "DBI:mysql:host=localhost;database=lichenfive";
	my $sthGetTax = $dbh->prepare("SELECT taxcd, syncd, genus, species, 
common, taxa, growthform, photobiont, abundance, status, photo, photographer, 
thumbmaps, Gallery, Sortor, Wisc_Found FROM spdetail WHERE Taxcd = '$taxcd' 
AND syncd = '$syncd' ORDER BY taxcd, syncd");
	$sthGetTax->execute();
	while (my ($taxcd, $syncd, $genus, $species, $common, $taxa,
$growthform, $photobiont, $abundance, $status_code, $photo, $photographer, 
$thumbmaps, $Gallery, $Sortorder, $Wisc_found) = $sthGetTax->fetchrow_array ()){
		$taxonName = $taxa;
	}
	return($taxonName);
}
