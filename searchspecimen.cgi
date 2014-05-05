#!/usr/bin/perl
# searchspecimen.cgi - wisflora specimen records listing
use strict;
use warnings;
use CGI;
use DBI;
use URI::URL;
my $title = "searchspecimen.cgi";
my $cgi = new CGI();
print $cgi->header(); 
print $cgi->start_html(-title => $title, -bgcolor => "white");
my $dsn = "DBI:mysql:host=localhost;database=herbfortynine";
my $dbhone = DBI->connect($dsn, "apache", "apachePASS") or die "cantconnect $!";
my $SpCodeParam = $cgi->param("SpCode");
#110508-this is for the click-to-sort visits from long-form resultsets
#my $SpCodeParam = $cgi->param("taxonParam");
my $GenusParam = $cgi->param("Genus");
my $FamilyParam = $cgi->param("Family");
my $SpeciesParam = $cgi->param("Species");
my $CommonParam = $cgi->param("Common");
#these next two variables are set by the query strings for type specimen and for endangered specimens
my $typeSpecimenParam = $cgi->param("typeSpecimen");
my $endangeredParam = $cgi->param("endangered");
my $WildcardParam;
my $bgcolor = "white";
my $familyName = "";
my $taxonName = "";
#these are potential params sent by searchspecimen.html
my $taxon; 
my $Genus; 
my $Species; 
my $Place; 
my $Town; 
my $Range; 
my $Section; 
my $txtSearchAccesssion; 
my $County; 
my $txtSearchCountry;
my $txtSearchHabitat; 
my $Collector;
my $Collevent; 
my $chkSearchType; 
my $chkSearchScan;
my $sortop;
my $sortdir;
my $taxonParam = ""; 
my $PlaceParam = ""; 
my $TownParam = ""; 
my $RangeParam = ""; 
my $SectionParam = ""; 
my $txtSearchAccessionParam = ""; 
my $CountyParam = ""; 
my $txtSearchCountryParam = "";
my $txtSearchHabitatParam = ""; 
my $CollectorParam = "";
my $ColleventParam = ""; 
my $chkSearchTypeParam = ""; 
my $chkSearchScanParam = "";
my $sortopParam = "";
my $sortdirParam = "";
my $taxcdParam = "";
#this new $COLLDATEWEB will hold a copy we can make 
# formatted for humans:
my $COLLDATEWEB = "";
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

{ # begin scope
	#Capture type-specimen queries first:
	if($typeSpecimenParam = $cgi->param("typeSpecimen")){
		#typeSpecimen is set, and so run type specimen sql and printout
		print $cgi->h2("Type Specimens");
		my $sthone = $dbhone->prepare ("SELECT specimen.ACCESSION, specimen.TAXCD, spdetail.Taxa FROM specimen INNER JOIN spdetail ON specimen.TAXCD = spdetail.Taxcd WHERE (spdetail.syncd='.' AND specimen.TYPE <> ' ' AND specimen.scan ='1') ORDER BY spdetail.Taxa, specimen.ACCESSION");
		$sthone->execute();
		my @rows = ();
		push (@rows, $cgi->Tr (
		              $cgi->th ({-bgcolor => $bgcolor}, "Taxon"),
		              $cgi->th ({-bgcolor => $bgcolor}, "Accession")
		            ));
	 	while (my ($ACCESSION, $Taxcd, $Taxa) = $sthone->fetchrow_array ()){
			# toggle the row-color variable
		 	$bgcolor = ($bgcolor eq "silver" ? "white" : "silver");
			push (@rows, $cgi->Tr (
		                $cgi->td({-bgcolor => $bgcolor}, $cgi->a({-href => "/cgi-bin/specimen.cgi?Accession=$ACCESSION"}, CGI::escapeHTML ($Taxa))),
		                $cgi->td({-bgcolor => $bgcolor}, $cgi->a({-href => "/cgi-bin/specimen.cgi?Accession=$ACCESSION"}, CGI::escapeHTML ($ACCESSION)))
		         ));
		#END while
		}
		print $cgi->table({-border => "1"}, @rows);
          
	#Capture endangered queries second:
	}elsif($endangeredParam = $cgi->param("endangered")){
		#endangered is set, and so run type specimen sql and printout
		print $cgi->h2("Endangered Specimens");
		my $sthone = $dbhone->prepare ("SELECT specimen.ACCESSION, specimen.TAXCD, spdetail.Taxa FROM specimen INNER JOIN spdetail ON specimen.TAXCD=spdetail.Taxcd WHERE specimen.Scan = '1' AND spdetail.Syncd='.' ORDER BY spdetail.Taxa, specimen.ACCESSION");
		$sthone->execute();
		my @rows = ();
		push (@rows, $cgi->Tr (
		              $cgi->th ({-bgcolor => $bgcolor}, "Taxon"),
		              $cgi->th ({-bgcolor => $bgcolor}, "Accession")
		            ));
	 	while (my ($ACCESSION, $TAXCD, $Taxa) = $sthone->fetchrow_array ()){
			my $sthtwo = $dbhone->prepare("SELECT Status, origin, status_code FROM spdetail WHERE Taxcd = '$TAXCD' AND Syncd = '.'");
			$sthtwo->execute();
			my $isItEndangered = 0;
	 		while (my ($Status, $origin, $status_code) = $sthtwo->fetchrow_array ()){
        			if($Status ne ""){
                			if($Status=~/Special Concern/){$isItEndangered = 1;}
                			if($Status=~/Endangered/){$isItEndangered = 1;}
                			if($Status=~/Threatened/){$isItEndangered = 1;}
                			if($Status=~/Extirpated/){$isItEndangered = 1;}
				}
	        		if($origin=~/Native/){
	                		if($status_code=~/BGC/){$isItEndangered = 1;}
	                		if($status_code=~/BGE/){$isItEndangered = 1;}
	                		if($status_code=~/BGT/){$isItEndangered = 1;}
	                		if($status_code=~/BSC/){$isItEndangered = 1;}
	                		if($status_code=~/BSE/){$isItEndangered = 1;}
	                		if($status_code=~/BSS/){$isItEndangered = 1;}
	                		if($status_code=~/BST/){$isItEndangered = 1;}
	                		if($status_code=~/C/){$isItEndangered = 1;}
	                		if($status_code=~/E/){$isItEndangered = 1;}
	                		if($status_code=~/F/){$isItEndangered = 1;}
	                		if($status_code=~/t/){$isItEndangered = 1;}
	                		if($status_code=~/T/){$isItEndangered = 1;}
				}elsif($origin=~/Introduced/){
	                		if($status_code=~/G/){$isItEndangered = 1;}
	                		if($status_code=~/L/){$isItEndangered = 1;}
	                		if($status_code=~/A/){$isItEndangered = 1;}
	                		if($status_code=~/AB/){$isItEndangered = 1;}
				}
			}
			if($isItEndangered == 1){  
			#if its endangered, then print the row!
				# toggle the row-color variable
		 		$bgcolor = ($bgcolor eq "silver" ? "white" : "silver");
				push (@rows, $cgi->Tr (
		                	$cgi->td({-bgcolor => $bgcolor}, $cgi->a({-href => "/cgi-bin/specimen.cgi?Accession=$ACCESSION"}, CGI::escapeHTML ($Taxa))),
		                	$cgi->td({-bgcolor => $bgcolor}, $cgi->a({-href => "/cgi-bin/specimen.cgi?Accession=$ACCESSION"}, CGI::escapeHTML ($ACCESSION))),
		         	));
			}
		#END while
		}
		print $cgi->table({-border => "1"}, @rows);
	#Capture long-form searchSpecimen.html queries third:
	}elsif($WildcardParam = $cgi->param("Wildcard")) {
		
		my $sqlxxx .= "SELECT * from t_vascular_common_names;";
		my $sthxxx = $dbhone->prepare ($sqlxxx);
		$sthxxx->execute();
		#the parameter named "Wildcard" (sent by form at specimenSearch.html) is 
		# actually a hidden form variable whose value is "True", whether that means 
		# a string or a boolean true or what, I'm not sure.  So this logic needs to 
		# be watched for unwanted behavior (i.e. cgi->param("Wildcard") returns weird)
		#since $wildcardParam exists, we were likely called from specimenSearch.html
		#taxon Genus Species Place Town Range Section txtSearchAccesssion County txtSearchCountry
		# txtSearchHabitat Collector Collevent Sortop chkSearchType chkSearchScan	
		my $sqlone = "SELECT * FROM specimen, spdetail WHERE spdetail.syncd = '.' ";
		#$get_querystring $gqs is a growing variuable that will hold the querystring we can use 
		# to reconstruct the POST request.  Since POST vars are not in the querystring, we 
		# can save them and use them to construct a querystring that will cause the same 
		# query to be run but via a querystring.  This is necessary because users want to 
		# sort these queryies by the column ...but by the time they want to click-to-sort 
		# we are no longer in a post situation.  And so we'll reconstruct t he POST request 
		# as a querystring get request.  The db query will be the same but thee sort order 
		# param will differ.
		my $gqs = "";
		#add wildard onto the query so that we revisit this "WILDARD " section.
		$gqs .= '&';
		$gqs .= 'Wildcard=';
		$gqs .= 'True';
		#notice that taxon and Taxa are not the same:
		if($taxonParam = $cgi->param("taxon")){ $gqs .= '&' ; $gqs .= "taxon"; $gqs .= '='; $gqs .= $taxonParam;
		       $taxonParam .= '%'; $sqlone .= " AND spdetail.Taxa LIKE '$taxonParam' ";
		}else{
		        $taxonParam= "";
		}
		if($taxcdParam = $cgi->param("taxcd")){ $gqs .= '&' ; $gqs .= "taxcd"; $gqs .= '='; $gqs .= $taxcdParam;
		       $taxcdParam .= '%'; $sqlone .= " AND spdetail.Taxcd LIKE '$taxcdParam' ";
		}else{
		        $taxcdParam= "";
		}
		if($GenusParam = $cgi->param("Genus")){ $gqs .= '&' ; $gqs .= "Genus"; $gqs .= '='; $gqs .= $GenusParam;
		       $GenusParam .= '%'; $sqlone .= " AND spdetail.Genus LIKE '$GenusParam' ";
		}else{
		        $GenusParam= "";
		}
		if($SpeciesParam = $cgi->param("Species")){ $gqs .= '&' ; $gqs .= "Species"; $gqs .= '='; $gqs .= $SpeciesParam;
		       $SpeciesParam .= '%'; $sqlone .= " AND spdetail.Species LIKE '$SpeciesParam' ";
		}else{
		        $SpeciesParam= "";
		}
		if($PlaceParam = $cgi->param("Place")){ $gqs .= '&' ; $gqs .= "Place"; $gqs .= '='; $gqs .= $PlaceParam;
		       $PlaceParam .= '%'; $sqlone .= " AND specimen.Place LIKE '$PlaceParam' ";
		}else{
		        $PlaceParam= "";
		}
		if($TownParam = $cgi->param("Town")){ $gqs .= '&' ; $gqs .= "Town"; $gqs .= '='; $gqs .= $TownParam;
		       $TownParam .= '%'; $sqlone .= " AND (specimen.T1 LIKE '$TownParam' OR specimen.T2 LIKE '$TownParam') ";
		}else{
		        $TownParam= "";
		}
		if($RangeParam = $cgi->param("Range")){ $gqs .= '&' ; $gqs .= "Range"; $gqs .= '='; $gqs .= $RangeParam;
		       $RangeParam .= '%'; $sqlone .= " AND (specimen.R1 LIKE '$RangeParam' OR specimen.R2 LIKE '$RangeParam') ";
		}else{
		        $RangeParam= "";
		}
		if($SectionParam = $cgi->param("Section")){ $gqs .= '&' ; $gqs .= "Section"; $gqs .= '='; $gqs .= $SectionParam;
		       $SectionParam .= '%'; $sqlone .= " AND (specimen.S1 LIKE '$SectionParam' OR specimen.S2 LIKE '$SectionParam') ";
		}else{
		        $SectionParam= "";
		}
		if($txtSearchAccessionParam = $cgi->param("txtSearchAccession")){ $gqs .= '&' ; $gqs .= "txtSearchAccession"; $gqs .= '='; $gqs .= $txtSearchAccessionParam;
		       $txtSearchAccessionParam .= '%'; $sqlone .= " AND specimen.ACCESSION LIKE '$txtSearchAccessionParam' ";
		}else{
		        $txtSearchAccessionParam= "";
		}
		if($CountyParam = $cgi->param("County")){ $gqs .= '&' ; $gqs .= "County"; $gqs .= '='; $gqs .= $CountyParam;
		       $CountyParam .= '%'; $sqlone .= " AND specimen.County LIKE '$CountyParam' ";
		}else{
		        $CountyParam= "";
		}
		if($txtSearchCountryParam = $cgi->param("txtSearchCountry")){ $gqs .= '&' ; $gqs .= "txtSearchCountry"; $gqs .= '='; $gqs .= $txtSearchCountryParam;
		       $txtSearchCountryParam .= '%'; $sqlone .= " AND specimen.Country LIKE '$txtSearchCountryParam' ";
		}else{
		        $txtSearchCountryParam= "";
		}
		if($txtSearchHabitatParam = $cgi->param("txtSearchHabitat")){ $gqs .= '&' ; $gqs .= "txtSearchHabitat"; $gqs .= '='; $gqs .= $txtSearchHabitatParam;
		       $txtSearchHabitatParam .= '%'; $sqlone .= " AND (specimen.Habitat LIKE '$txtSearchHabitatParam' OR specimen.Habitat_MISC LIKE '$txtSearchHabitatParam') ";
		}else{
		        $txtSearchHabitatParam= "";
		}
		if($CollectorParam = $cgi->param("Collector")){ $gqs .= '&' ; $gqs .= "Collector"; $gqs .= '='; $gqs .= $CollectorParam;
		       $CollectorParam .= '%'; $sqlone .= " AND specimen.Coll1Name LIKE '$CollectorParam' ";
		}else{
		        $CollectorParam= "";
		}
		if($ColleventParam = $cgi->param("Collevent")){ $gqs .= '&' ; $gqs .= "Collevent"; $gqs .= '='; $gqs .= $ColleventParam;
		       $ColleventParam .= '%'; $sqlone .= " AND specimen.Collevent LIKE '$ColleventParam' ";
		}else{
		        $ColleventParam= "";
		}
		if($chkSearchTypeParam = $cgi->param("chkSearchType")){ $gqs .= '&' ; $gqs .= "chkSearchType"; $gqs .= '='; $gqs .= $chkSearchTypeParam;
		       $chkSearchTypeParam .= '%'; $sqlone .= " AND specimen.Type IS NOT NULL' ";
		}else{
		        $chkSearchTypeParam= "";
		}
		if($chkSearchScanParam = $cgi->param("chkSearchScan")){ $gqs .= '&' ; $gqs .= "chkSearchScan"; $gqs .= '='; $gqs .= $chkSearchScanParam;
		       $chkSearchScanParam .= '%'; $sqlone .= " AND specimen.Scan IS NOT NULL";
		}else{
		        $chkSearchScanParam= "";
		}
		#   SORT START######################
		if($sortop = $cgi->param("sortop")){
			#$gqs .= '&' ; $gqs .= "sortop"; $gqs .= '='; $gqs .= $sortop;
			;
		}else{
			$sortop = 'ACCESSION';
		}
		#   SORT STOP   #############
		$sortdir = 'ASC';
		$sqlone .= " AND specimen.TAXCD = spdetail.Taxcd ORDER BY $sortop $sortdir";
		my $sthone = $dbhone->prepare ($sqlone);
		$sthone->execute();
		my @rows = ();
		#Check ENV hash to learn what current URL is...we could also use CGI::url()
		my $url_base = $ENV{SCRIPT_NAME};
		#110508
		#my $query_str = $ENV{QUERY_STRING};
		#my $url_complete = $url_base.'?'.$query_str;
		my $url_complete = $url_base.'?';
		my $url_complete_without_sortop = $url_complete;
		$url_complete_without_sortop=~s/.sortop.*//g;
		push (@rows, $cgi->Tr (
		              $cgi->th ({-bgcolor => $bgcolor}, $cgi->a({-href => "$url_complete_without_sortop"."sortop=ACCESSION".$gqs}, "Accession")),
		              $cgi->th ({-bgcolor => $bgcolor}, $cgi->a({-href => "$url_complete_without_sortop"."sortop=spdetail.Taxcd".$gqs}, "Taxon")),
		              $cgi->th ({-bgcolor => $bgcolor}, $cgi->a({-href => "$url_complete_without_sortop"."sortop=COLLDATE".$gqs}, "Date")),
		              $cgi->th ({-bgcolor => $bgcolor}, $cgi->a({-href => "$url_complete_without_sortop"."sortop=COLL1NAME".$gqs}, "Collector")),
		              $cgi->th ({-bgcolor => $bgcolor}, $cgi->a({-href => "$url_complete_without_sortop"."sortop=COLLNO1".$gqs}, "Coll No.")),
		              $cgi->th ({-bgcolor => $bgcolor}, $cgi->a({-href => "$url_complete_without_sortop"."sortop=COUNTY".$gqs}, "County")),

		            ));

#		push (@rows, $cgi->Tr (
#		              $cgi->th ({-bgcolor => $bgcolor}, $cgi->a({-href => "$ENV{SCRIPT_NAME}.&sortop=Accession"}, "Accession")),
#		              $cgi->th ({-bgcolor => $bgcolor}, "Taxon"),
#		              $cgi->th ({-bgcolor => $bgcolor}, "Date"),
#		              $cgi->th ({-bgcolor => $bgcolor}, "Collector"),
#		              $cgi->th ({-bgcolor => $bgcolor}, "Coll.No."),
#		              $cgi->th ({-bgcolor => $bgcolor}, "County")
#		            ));

		#while(my ($ACCESSION, $TYPE, $COLLDATE, $FLOWER, $FRUIT, $STERILE, $OBJTYPE, $INST, $ANNCODE, $ANNDATE, $ANNSOURCE, $CITY, $SITENO, $CITYTYPE, $COLL2NAME, $COLL3NAME, $COLL1NAME, $COLLNO1, $COLLEVENT, $TAXCD, $CFS, $CFV, $CFVariety, $HABITAT_MISC, $HABITAT, $LONGX, $LAT, $ELEV, $LLGENER, $LONG2, $LAT2, $LTDEC, $LGDEC, $NOWLOC, $LOAN, $PAGES, $ORIGCD, $PUBCD, $LITCIT, $PUBDATE, $PUBDATEA, $VERPERS, $VERDATE, $EX, $ARTICLE, $PREC, $STATEL, $COUNTY, $COUNTRY, $T1, $R1, $S1, $NSEW_1, $TRSGENER, $T2, $R2, $S2, $NSEW_2, $PLACE, $scan, $MAPFILE, $username, $date_time, $DTRS, $specimen_PKID, $specimen_CHANGETIME, $Taxcd, $Syncd, $family_code, $genus, $species, $authority, $subsp, $variety, $forma, $subsp_auth, $var_auth, $forma_auth, $sub_family, $tribe, $common, $Wisc_found, $ssp, $var, $f, $hybrids, $status_code, $hide, $USDA, $COFC, $WETINDICAT, $FAM_NAME, $FAMILY, $GC, $FAMILY_COMMON, $SYNWisc_found, $SYNS_STATUS, $SYNV_STATUS, $SYNF_STATUS, $SYNHYBRIDS_STATUS, $SYNW_STATUS, $speciesweb_Taxcd, $Status, $Photo, $Photographer, $Thumbmaps, $Accgenus, $SORTOR, $Hand, $growth_habit_bck, $blooming_dt_bck, $origin_bck, $Thumbphoto, $date_time_TWO, $growth_habit, $blooming_dt, $origin, $Taxa) = $sthone->fetchrow_array()){
#110508
#This while loop does not have the CHANGETIME thing because it runs on MySQL 3.s23 and so doesn't have changeime
		while(my ($ACCESSION, $TYPE, $COLLDATE, $FLOWER, $FRUIT, $STERILE, $OBJTYPE, $INST, $ANNCODE, $ANNDATE, $ANNSOURCE, $CITY, $SITENO, $CITYTYPE, $COLL2NAME, $COLL3NAME, $COLL1NAME, $COLLNO1, $COLLEVENT, $TAXCD, $CFS, $CFV, $CFVariety, $HABITAT_MISC, $HABITAT, $LONGX, $LAT, $ELEV, $LLGENER, $LONG2, $LAT2, $LTDEC, $LGDEC, $NOWLOC, $LOAN, $PAGES, $ORIGCD, $PUBCD, $LITCIT, $PUBDATE, $PUBDATEA, $VERPERS, $VERDATE, $EX, $ARTICLE, $PREC, $STATEL, $COUNTY, $COUNTRY, $T1, $R1, $S1, $NSEW_1, $TRSGENER, $T2, $R2, $S2, $NSEW_2, $PLACE, $scan, $MAPFILE, $username, $date_time, $DTRS, $specimen_PKID, $Taxcd, $Syncd, $family_code, $genus, $species, $authority, $subsp, $variety, $forma, $subsp_auth, $var_auth, $forma_auth, $sub_family, $tribe, $common, $Wisc_found, $ssp, $var, $f, $hybrids, $status_code, $hide, $USDA, $COFC, $WETINDICAT, $FAM_NAME, $FAMILY, $GC, $FAMILY_COMMON, $SYNWisc_found, $SYNS_STATUS, $SYNV_STATUS, $SYNF_STATUS, $SYNHYBRIDS_STATUS, $SYNW_STATUS, $speciesweb_Taxcd, $Status, $Photo, $Photographer, $Thumbmaps, $Accgenus, $SORTOR, $Hand, $growth_habit_bck, $blooming_dt_bck, $origin_bck, $Thumbphoto, $date_time_TWO, $growth_habit, $blooming_dt, $origin, $Taxa) = $sthone->fetchrow_array()){
			#$sthtwo is run so that we can obtain the "Taxa" name from spdetail for this particular specimen:
			#notice that this next query has strong potential for being rerun over-and-over-and-over again, room for improvement here:
			#my $sthtwo = $dbhone->prepare ("SELECT Taxa, FAMILY FROM spdetail WHERE Taxcd = '$SpCodeParam' AND Syncd = '.'");
			my $sthtwo = $dbhone->prepare ("SELECT Taxa, FAMILY FROM spdetail WHERE Taxcd = '$Taxcd' AND Syncd = '.'");
			$sthtwo->execute();
			while (my ($Taxa, $Family) = $sthtwo->fetchrow_array ()){
				#nothing to do, we've got the data for the species linkback
				$familyName = $Family;
				$taxonName = $Taxa;
			}
			$COLLDATE=~s/00:00:00//g;
			$COLLDATE=~s/0:00:00//g;
		 	$bgcolor = ($bgcolor eq "silver" ? "white" : "silver");
			push (@rows, $cgi->Tr (
		                $cgi->td({-bgcolor => $bgcolor}, $cgi->a({-href => "/cgi-bin/specimen.cgi?Accession=$ACCESSION"}, CGI::escapeHTML ($ACCESSION))),
		                $cgi->td({-bgcolor => $bgcolor}, $cgi->a({-href => "/cgi-bin/detail.cgi?SpCode=$TAXCD"}, CGI::escapeHTML($taxonName))),
		                $cgi->td({-bgcolor => $bgcolor}, CGI::escapeHTML ($COLLDATE)),
		                $cgi->td({-bgcolor => $bgcolor}, CGI::escapeHTML ($COLL1NAME)),
		                $cgi->td({-bgcolor => $bgcolor}, CGI::escapeHTML ($COLLNO1)),
		                $cgi->td({-bgcolor => $bgcolor}, CGI::escapeHTML ($COUNTY))
		         ));
		#END while
		}
		print $cgi->table({-border => "1"}, @rows);
	}else{
		#   SORT START######################
		#020908...here we ensure we've gathered proper data into $sortop variable 
		#which we'll use for the 'ORDER BY' clause of the SQL query:
		if($sortop = $cgi->param("sortop")){
			if($sortop=~/COLLDATE/){
				$sortop = " rcoll, lcoll, COLLDATE ";
			}else{
				;
			}
		}else{
			$sortop = 'ACCESSION';
		}
		# SORT STOP #############
	#This is the logic that will be followed by the vast majority of script executions.  
	#The above if clauses look for special cases of endangered, type-specimen, long-form, 
	#respectively.  Notice that all three special cases are accessed by using an 
	#unusual form.  The typical case is handled by this logic, and this logic is executed 
	#each time someone clicks on the famous "View Herbarium Records" link on detail.cgi.
	#Because searches using this script are dominated by the normal access method, we can 
	#likely get away with metering records for this logic only, and just let the other pages 
	#go long.  The long-form result page will also need metering, since those queries often 
	#run long result sets.
		#METERING CODE
		#To meter pages, we need to know 3 things:
		#1. How many records are there
		#2. How many records per page do you want to see.
		#3. Which page are we on now?

		my $start = $cgi->param ("start");
		if(!defined ($start) || $start !~ /^\d+$/ || $start < 1) {
			$start = 1;
		}
		my $per_page = $cgi->param ("per_page");
		if(!defined ($per_page) || $per_page !~ /^\d+$/ || $per_page < 1){
			$per_page = 100;
		}
		#no need for the 'ORDER BY' clause on previous commented line, so instead:
		my $total_recs = $dbhone->selectrow_array ("SELECT COUNT(*) FROM specimen WHERE taxcd = '$SpCodeParam'");
		#METERING CODE
		#Feb0908...change for sortop ordering
		#ensure $sortop makes sense, or is ACCESSION
		#unless($sortop){$sortop = 'ACCESSION'}
		#my $stmt = sprintf ("SELECT * FROM specimen WHERE taxcd = '$SpCodeParam' ORDER BY $sortop LIMIT %d,%d", $start-1, $per_page);
		my $stmt = sprintf ("SELECT *, LEFT(RIGHT(COLLDATE,12), 4) rcoll, RIGHT(LEFT(COLLDATE,2),1) lcoll FROM specimen WHERE taxcd = '$SpCodeParam' ORDER BY $sortop LIMIT %d,%d", $start-1, $per_page);
		my $sthone = $dbhone->prepare ($stmt);
		$sthone->execute();
		my @rows = ();
		#Check ENV hash to learn what current URL is...we could also use CGI::url()
		my $url_base = $ENV{SCRIPT_NAME};
		my $query_str = $ENV{QUERY_STRING};
		my $url_complete = $url_base.'?'.$query_str;
		my $url_complete_without_sortop = $url_complete;
		$url_complete_without_sortop=~s/.sortop.*//g;
		push (@rows, $cgi->Tr (
		              $cgi->th ({-bgcolor => $bgcolor}, $cgi->a({-href => "$url_complete_without_sortop&sortop=Accession"}, "Accession")),
		              $cgi->th ({-bgcolor => $bgcolor}, $cgi->a({-href => "$url_complete_without_sortop&sortop=Taxcd"}, "Taxon")),
		              $cgi->th ({-bgcolor => $bgcolor}, $cgi->a({-href => "$url_complete_without_sortop&sortop=COLLDATE"}, "Date")),
		              $cgi->th ({-bgcolor => $bgcolor}, $cgi->a({-href => "$url_complete_without_sortop&sortop=COLL1NAME"}, "Collector")),
		              $cgi->th ({-bgcolor => $bgcolor}, $cgi->a({-href => "$url_complete_without_sortop&sortop=COLLNO1"}, "Coll No.")),
		              $cgi->th ({-bgcolor => $bgcolor}, $cgi->a({-href => "$url_complete_without_sortop&sortop=COUNTY"}, "County")),

		            ));
		#run while loop...but isn't it (now) true that $id, the last variable will be 
		# empty because the db won't return that many fields.
	 	while (my ($ACCESSION, $TYPE, $COLLDATE, $FLOWER, $FRUIT, $STERILE, $OBJTYPE, $INST, $ANNCODE, $ANNDATE, $ANNSOURCE, $CITY, $SITENO, $CITYTYPE, $COLL2NAME, $COLL3NAME, $COLL1NAME, $COLLNO1, $COLLEVENT, $TAXCD, $CFS, $CFV, $CFVariety, $HABITAT_MISC, $HABITAT, $LONGX, $LAT, $ELEV, $LLGENER, $LONG2, $LAT2, $LTDEC, $LGDEC, $NOWLOC, $LOAN, $PAGES, $ORIGCD, $PUBCD, $LITCIT, $PUBDATE, $PUBDATEA, $VERPERS, $VERDATE, $EX, $ARTICLE, $PREC, $STATEL, $COUNTY, $COUNTRY, $T1, $R1, $S1, $NSEW_1, $TRSGENER, $T2, $R2, $S2, $NSEW_2, $PLACE, $scan, $MAPFILE, $username, $date_time, $DTRS, $id) = $sthone->fetchrow_array ()){
			#$sthtwo is run so that we can obtain the "Taxa" name from spdetail for this particular specimen:
			#notice that this next query has strong potential for being rerun over-and-over-and-over again, room for improvement here:
			my $sthtwo = $dbhone->prepare ("SELECT Taxa, FAMILY FROM spdetail WHERE Taxcd = '$SpCodeParam' AND Syncd = '.'");
			$sthtwo->execute();
			while (my ($Taxa, $Family) = $sthtwo->fetchrow_array ()){
				#nothing to do, we've got the data for the species linkback
				$familyName = $Family;
				$taxonName = $Taxa;
			}
			$COLLDATE=~s/00:00:00//g;
			$COLLDATE=~s/0:00:00//g;
			# toggle the row-color variable
		 	$bgcolor = ($bgcolor eq "silver" ? "white" : "silver");
			push (@rows, $cgi->Tr (
		                $cgi->td({-bgcolor => $bgcolor}, $cgi->a({-href => "/cgi-bin/specimen.cgi?Accession=$ACCESSION"}, CGI::escapeHTML ($ACCESSION))),
		                $cgi->td({-bgcolor => $bgcolor}, $cgi->a({-href => "/cgi-bin/detail.cgi?SpCode=$SpCodeParam"}, CGI::escapeHTML($taxonName))),
		                $cgi->td({-bgcolor => $bgcolor}, CGI::escapeHTML ($COLLDATE)),
		                $cgi->td({-bgcolor => $bgcolor}, CGI::escapeHTML ($COLL1NAME)),
		                $cgi->td({-bgcolor => $bgcolor}, CGI::escapeHTML ($COLLNO1)),
		                $cgi->td({-bgcolor => $bgcolor}, CGI::escapeHTML ($COUNTY))
		         ));
		#END while
		}
		print $cgi->table({-border => "1"}, @rows);
	#END if(wildcard)
		#METERCODE
		for (my $first = 1; $first <= $total_recs; $first += $per_page){
			my $last = $first + $per_page - 1;
			$last = $total_recs if $last > $total_recs;
		  	my $label = "$first to $last";
		  	my $link;
			#newfangled uri object:
			#my $u =  URI::URL->new("http://www.botany.wisc.edu/cgi-bin/searchspecimen.cgi?"."$ENV{QUERY_STRING}");
			my $u =  URI::URL->new("http://www.botany.wisc.edu/cgi-bin/searchspecimen.cgi?"."$ENV{QUERY_STRING}");

			# live link
		  	if ($first != $start){
				my $utwo = $u->clone();
				$utwo=~s/.start.*//g;
		    		#my $url = sprintf ("%s&start=%d&per_page=%d", $utwo, $first, $per_page);
		    		my $url = sprintf ("%s&start=%d&per_page=%d&sortop=$sortop", $utwo, $first, $per_page);
		    		#$link = $cgi->a({-href => $url}, $label);
		    		$link = $cgi->a({-href => $url}, $label);

	               	# static text
		  	}else{
		    		$link = $label;
			}
		  	print("[$link] ");
		}#endfor()
		print("Total Records: $total_recs");
		print("<BR><BR> <a href=\"http:\/\/www.botany.wisc.edu\/cgi-bin\/excel_maker_custom.cgi?SpCode=$SpCodeParam\">Download specimen result set as Excel spreadsheet<\/a><BR>");
		#METERCODE
	}
} # end scope

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

$dbhone->disconnect ();
print $cgi->end_html();
exit (0);

# _MAKE_TABLE_FROM_QUERY_
# temp table used to display output from queries:
sub make_table_from_query
{
# db handle, query string, parameters to be bound to placeholders (if any)
my ($dbh, $stmt, @param) = @_;

  my $sth = $dbh->prepare ($stmt);
  $sth->execute (@param);
  my @rows = ();
  # use column names for cells in the header row
  push (@rows, $cgi->Tr($cgi->th ([ map { CGI::escapeHTML($_) } @{$sth->{NAME}} ])));
  # fetch each data row
  while (my $row_ref = $sth->fetchrow_arrayref ())
  {
    # encode cell values, avoiding warnings for undefined
    # values and using &nbsp; for empty cells
    my @val = map {
                defined ($_) && $_ !~ /^\s*$/ ? CGI::escapeHTML($_) : "&nbsp;"
              } @{$row_ref};
    my $row_str;
    for (my $i = 0; $i < @val; $i++)
    {
      # right-justify numeric columns
      if ($sth->{mysql_is_num}->[$i])
      {
        $row_str .= $cgi->td ({-align => "right"}, $val[$i]);
      }
      else
      {
        $row_str .= $cgi->td ($val[$i]);
      }
    }
    push (@rows, $cgi->Tr($row_str));
  }
  return ($cgi->table ({-border => "1"}, @rows));
}
__DATA__
