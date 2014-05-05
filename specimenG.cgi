#!/usr/bin/perl
# specimen.cgi - wisflora specimen record information
use strict;
use warnings;
use CGI;
use DBI;
use URI::URL;
my $title = "specimen.cgi";
my $cgi = new CGI();
print $cgi->header(); 
my $AccessionParamgmap = $cgi->param("Accession");
my $dsn = "DBI:mysql:host=localhost;database=herbfortynine";
my $dbh = DBI->connect($dsn, "apache", "apachePASS") or die "cantconnect $!";
my $sthgmap = $dbh->prepare ("SELECT TAXCD, LTDEC, LGDEC FROM specimen WHERE ACCESSION = '$AccessionParamgmap'");
$sthgmap->execute();
my $LTDECgmapGlobal;
my $LGDECgmapGlobal;
my $taxcdGglobal;
while (my ($taxcdG, $LTDECgmap, $LGDECgmap) = $sthgmap->fetchrow_array ()){
$LTDECgmapGlobal = $LTDECgmap;
$LGDECgmapGlobal = $LGDECgmap;
$taxcdGglobal = $taxcdG;
}

#this query finds if the species is hidden...if so, there should be no googleMap, and this quells the map printout:
my $sthgmaptwo = $dbh->prepare ("SELECT Taxcd, hide FROM spdetail WHERE Taxcd = '$taxcdGglobal' AND Syncd = '.'");
$sthgmaptwo->execute();
while (my ($taxcdGtwo, $hideG) = $sthgmaptwo->fetchrow_array ()){
	if($hideG=~/Y/) {
		#print("HIDE: $hideG");
		$LTDECgmapGlobal = '';
		$LGDECgmapGlobal = '';
	}
}

#print $cgi->start_html(-title => $title, -bgcolor => "white");

print("<body onload=\"load()\" onunload=\"GUnload()\" bgcolor=\"white\"><table width=\"100%\" border=\"0\" bgcolor=\"#EEEEEE\">\n");


print("<script src=\"http://maps.google.com/maps?file=api&amp;v=2&amp;key=ABQIAAAAmvMjxpMZ6TmaOCTn9rv-BRSx0q5GtAeRCBdJDmPd8o6P34PnHBRKcHVBTCS5bpzLT21zRXEEtPutEA\"\n");
print("type=\"text/javascript\"></script>\n");
print("<script type=\"text/javascript\">\n");
print("//<![CDATA[\n");
print("function load() {\n");
print("if (GBrowserIsCompatible()) {\n");
print("var map = new GMap2(document.getElementById(\"map\"));\n");
print("map.setCenter(new GLatLng($LTDECgmapGlobal, $LGDECgmapGlobal), 13);\n");
#print("map.setCenter(new GLatLng(43.0740, -89.4029), 17);\n");
print("map.addControl(new GSmallMapControl());\n");
print("var latlng = new GLatLng($LTDECgmapGlobal, $LGDECgmapGlobal);\n");
print("map.addOverlay(new GMarker(latlng));\n");
print("}\n");
print("}\n");
print("\n");
print("//]]>\n");
print("</script>\n");





#my $dsn = "DBI:mysql:host=localhost;database=herbforty";
#my $dbh = DBI->connect($dsn, "apache", "apachePASS") or die "cantconnect $!";
#my @params = param();
# The %Institution hash holds the mapping between the CODENAME of the 
# institution and the human-readable name.  This should be a table in 
# the database, and the database maybe perhaps should store the string 
# instead of using CODENAME indirection for no good reason.  In any, case,
# since the current database feeds us codes, we need a way to map those 
# codes to the human-readable meaning, and the way this program does it 
# is by using this %Institution hash to lookup the meaning of the CODE
# retrieved from the database:
my %Institution = (
	"BELC" => "Beloit College",         
	"CART" => "Carthage College",
        "MAD" => "Forest Products Laboratory",
        "MIL" => "Milwaukee Public Museum",
        "PTIS" => "Potato Introduction Station",
        "SNC" => "Saint Norbert College",         
	"FDLW" => "University of Wisconsin Center",
        "UWEC" => "University of Wisconsin-Eau Claire",         
	"UWGB" => "University of Wisconsin-Green Bay",         
	"UWL" => "University of Wisconsin-La Crosse",
        "WIS" => "University of Wisconsin-Madison",         
	"UWM" => "University of Wisconsin-Milwaukee",
        "OSH" => "University of Wisconsin Oshkosh",
        "RIVE" => "University of Wisconsin-River Falls",
        "SUWS" => "University of Wisconsin-Superior",
        "UWSP" => "University of Wisconsin-Stevens Point",
        "UWW" => "University of Wisconsin-Whitewater",
);
#Like the %Institution hash, we need an object-type hash, %kindOfSpecimen,
# to lookup the code from the database and print a human-readable meaning:
my %kindOfSpecimen = (
        "E" => "envelope/packet",
        "I" => "illustration",
        "L" => "letter",
        "M" => "mounted",
        "P" => "photo",
        "S" => "slide",
        "V" => "visual only",
        "X" => "xerox copy",
);
#Like the %Institution hash, we need a pop-area-type hash, %popAreaType,
# to lookup the code from the database and print a human-readable meaning:
my %popAreaType = (
        "C" => "City",
        "V" => "Village",
        "T" => "Town",
        "R" => "Locality",
        "I" => "Island",
);

#a flag to know whether the species under consideration is endangered:
my $isItEndangered = 0;




my $AccessionParam = $cgi->param("Accession");
my $typeSpecimenParam = $cgi->param("typeSpecimen");
my $endangeredSpecimenParam = $cgi->param("endangeredSpecimen");

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

print $cgi->h2("Specimen Detail Page");





{ # begin scope
	#otherwise its a straight ACCESSION lookup:
	my $sthone = $dbh->prepare ("SELECT * FROM specimen WHERE ACCESSION = '$AccessionParam'");
	$sthone->execute();
 	while (my ($ACCESSION, $TYPE, $COLLDATE, $FLOWER, $FRUIT, $STERILE, $OBJTYPE, $INST, $ANNCODE, $ANNDATE, $ANNSOURCE, $CITY, $SITENO, $CITYTYPE, $COLL2NAME, $COLL3NAME, $COLL1NAME, $COLLNO1, $COLLEVENT, $TAXCD, $CFS, $CFV, $CFVariety, $HABITAT_MISC, $HABITAT, $LONGX, $LAT, $ELEV, $LLGENER, $LONG2, $LAT2, $LTDEC, $LGDEC, $NOWLOC, $LOAN, $PAGES, $ORIGCD, $PUBCD, $LITCIT, $PUBDATE, $PUBDATEA, $VERPERS, $VERDATE, $EX, $ARTICLE, $PREC, $STATEL, $COUNTY, $COUNTRY, $T1, $R1, $S1, $NSEW_1, $TRSGENER, $T2, $R2, $S2, $NSEW_2, $PLACE, $scan, $MAPFILE, $username, $date_time, $DTRS, $specimen_id) = $sthone->fetchrow_array ()){


print<<"TABLETWO";
<table border="0" width="80%">
  <tr>
    <td width="96%"> <table border="0" width="100%">
        <tr>
          <td> <table border="0">
              <tr>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Accession:</b></font>&nbsp;
                </td>
                <td>
TABLETWO
print("$ACCESSION  &nbsp;&nbsp;&nbsp;&nbsp;");
print<<"TABLETHREE";
		</td>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Institution:</b></font>&nbsp;
                </td>
                <td colspan="3">
TABLETHREE
print("$Institution{$INST}");
print<<"TABLEFOUR";
</td>
              </tr>
              <tr>
                <td align="right" bgcolor="#EEEEEE"> <b><font size=2>Taxon Code:</font></b>&nbsp;
                </td>
                <td colspan="5">
TABLEFOUR
print("<a href=\"/cgi-bin/detail.cgi?SpCode=$TAXCD\">$TAXCD</a>");
print<<"TABLEFIVE";
                  </a> </td>
              </tr>
TABLEFIVE
	if($CFS ne "" or $CFV ne "" or $CFVariety ne "" ){
print<<"TABLESIX";
              <tr>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Aff./Cf.
                  Species:</b></font>&nbsp; </td>
                <td> 
TABLESIX
print("$CFS"); 
print<<"TABLESEVEN";
</td>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Aff./Cf.
                  Sub-Species:</b></font>&nbsp; </td>
                <td> 
TABLESEVEN
print("$CFV"); 
print<<"TABLEEIGHT";

</td>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Aff./Cf.
                  Variety:</b></font>&nbsp; </td>
                <td> 
TABLEEIGHT
print("$CFVariety"); 

print<<"TABLENINE";
</td>
              </tr>
TABLENINE
	}
print<<"TABLETEN";
              <tr>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Page per
                  Specimen:</b></font>&nbsp; </td>
                <td> 
TABLETEN
print("$PAGES");
print<<"TABLEELEVEN";
 	</td>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Kind Of Specimen:</b></font>&nbsp;
                </td>
                <td> 
TABLEELEVEN
print("$kindOfSpecimen{$OBJTYPE}");
#print("$OBJTYPE");
print<<"TABLETWELVE"; 
	</td>
                <td colspan="2">&nbsp; </td>
              </tr>
TABLETWELVE
	if($FLOWER ne "" or $FRUIT ne "" or $STERILE ne ""){
print<<"TABLETHIRTEEN"; 
              <tr>
                <td colspan="6">&nbsp; </td>
              </tr>
              <tr>
                <td colspan="6" align="center"> <table border="0">
                    <tr>
                      <td bgcolor="#EEEEEE"> <font size="2"><strong>Flower:</strong></font>&nbsp;
                      </td>
                      <td> 

TABLETHIRTEEN
print("$FLOWER");
print<<"TABLEFOURTEEN"; 
	</td>
                      <td> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </td>
                      <td bgcolor="#EEEEEE"> <font size="2"><strong>Fruit:</strong></font>&nbsp;
                      </td>
                      <td> 
TABLEFOURTEEN
print("$FRUIT"); 
print<<"TABLEFIFTEEN"; 
	</td>
                      <td> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; </td>
                      <td bgcolor="#EEEEEE"> <font size="2"><strong>Sterile:</strong></font>&nbsp;
                      </td>
                      <td> 
TABLEFIFTEEN
print("$STERILE");
print<<"TABLESIXTEEN"; 
 	</td>
                    </tr>
                  </table></td>
              </tr>
TABLESIXTEEN
	}
print<<"TABLESEVENTEEN"; 
            </table></td>
        </tr>
      </table>
 <br> </td>
    <td width="4%" rowspan="2" align="left" valign="top"> 
TABLESEVENTEEN


if ($scan == 1){
my $thumbname = "/herb/wwwherbarium/wisflora/pictures/specimenscans/200px/$ACCESSION"."thumb.jpg";
my $thumbURL = "/herbarium/wisflora/pictures/specimenscans/200px/$ACCESSION"."_thumb.jpg";
my $smallURL = "/herbarium/wisflora/pictures/specimenscans/500px/$ACCESSION"."_medium.jpg";
my $mediumURL = "/herbarium/wisflora/pictures/specimenscans/800px/$ACCESSION"."_large.jpg";
my $largeURL = "/herbarium/wisflora/pictures/specimenscans/full%20size/$ACCESSION".".jpg";

print("<TABLE border=0 align='center' valign='top'><tr><td>");
print("<br>Specimen Scan<br><FONT SIZE='-2' FACE='ARIAL, HELVETICA'><A HREF=\"$smallURL\"><IMG SRC=\"$thumbURL\"></A></font>");
print("<br><FONT SIZE='-2' FACE='ARIAL, HELVETICA'><A HREF=\"$mediumURL\">View Large Image</A></font>");
print("<br><FONT SIZE='-2' FACE='ARIAL, HELVETICA'><A HREF=\"$largeURL\">View X-Large Image</A></font>") ;
print("</td></tr></table>");
	}
print<<"TABLEEIGHTEEN"; 
                </td>
  </tr>
  <tr>
    <td> <table border=0>
        <tr>
          <td align="right" bgcolor="#EEEEEE" NOWRAP> <font size=2><b>Pop. Area:</b></font>&nbsp;
          </td>
          <td> 

TABLEEIGHTEEN
print("$CITY");
print<<"TABLENINETEEN"; 
</td>
          <td align="right" bgcolor="#EEEEEE" NOWRAP> <font size=2><b>Pop. Area
            Type:</b></font>&nbsp; </td>
          <td> 
TABLENINETEEN
#print(getcitytype("$CITYTYPE"));
print("$popAreaType{$CITYTYPE}");
#print("$CITYTYPE");
print<<"TABLETWENTY"; 
</td>
          <td colspan=2>&nbsp; </td>
        </tr>
        <tr>
          <td align="right" bgcolor="#EEEEEE" NOWRAP> <font size=2><b>State:</b></font>&nbsp;
          </td>
          <td> 
TABLETWENTY

print("$STATEL");
print<<"TABLETWENTYONE"; 
	</td>
          <td align="right" bgcolor="#EEEEEE"> <font size=2><b>County:</b></font>&nbsp;
          </td>
          <td> 
TABLETWENTYONE
print("$COUNTY");
print<<"TABLETWENTYTWO"; 
</td>
          <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Country:</b></font>&nbsp;
          </td>
          <td> 
TABLETWENTYTWO
print("$COUNTRY");
print<<"TABLETWENTYTHREE"; 
</td>
        </tr>
TABLETWENTYTHREE





#This query is the BROKEN112107 version of endangered protection.  The idea is 
# that the db should not reveal location-specific information about species that
# are endangered:

			my $sthfive = $dbh->prepare("SELECT Status, origin, status_code FROM spdetail WHERE Taxcd = '$TAXCD' AND Syncd = '.'");
                        $sthfive->execute();
                        $isItEndangered = 0;
                        while (my ($Status, $origin, $status_code) = $sthfive->fetchrow_array ()){                                if($Status ne ""){
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










if($isItEndangered == 0) {
print<<"TABLETWENTYFOUR"; 
<!--
        if (not isRestricted(RS("TAXCD"))) OR session("adminedit") = 1 then
-->
        <tr>
          <td align="right" bgcolor="#EEEEEE" NOWRAP> <font size=2><b>Site No.:</b></font>&nbsp;
          </td>
          <td colspan="5"> 
TABLETWENTYFOUR

#print("$SITENO");
#print("Tomgetsiteno($SITENO)");
#Another DB lookup is required to get the data related to $SITENO value from 
# the specimen table into a human-usable string by querying the sitelkup 
# table:
	my $sthfour = $dbh->prepare ("SELECT SPLACE STYPE FROM sitelkup WHERE SITENO = '$SITENO'");
	$sthfour->execute();
 	while (my ($SPLACE, $STYPE) = $sthfour->fetchrow_array ()){
		print("$SPLACE &nbsp;&nbsp; $STYPE");
		last;
	}

print<<"TABLETWENTYFIVE"; 
</td>
        </tr>
        <tr>
          <td align="right" bgcolor="#EEEEEE" NOWRAP> <font size="2"><b>Collection
            Event:</b></font>&nbsp; </td>
          <td colspan="5"> 
TABLETWENTYFIVE


#print("getCollEvent($COLLEVENT)");
#Another DB lookup is required to get the $COLLEVENT db returned value from 
# the specimen table into a human-usable string by querying the colleventlkup 
# table:
	my $sththree = $dbh->prepare ("SELECT Name FROM colleventlkup WHERE Collevent = '$COLLEVENT'");
	$sththree->execute();
 	while (my ($collectorName) = $sththree->fetchrow_array ()){
		print("$collectorName");
		last;
	}
print("$COLLEVENT");

print<<"TABLETWENTYSIX"; 
</td>
        </tr>
        <tr>
          <td align="right" valign="top" bgcolor="#EEEEEE"> <font size=2><b>Place:</b></font>&nbsp;
          </td>
          <td colspan=5> 
TABLETWENTYSIX

print("$PLACE");
#print("TOM-MakePlaceLookup($PLACE)");

print<<"TABLETWENTYSEVEN"; 
</td>
        </tr>
        <tr>
          <td colspan=6>&nbsp; </td>
        </tr>
        <tr>
          <td>&nbsp; </td>
          <td colspan=5> <table border=0>
TABLETWENTYSEVEN



	if($T1 ne "" or $R1 ne "" or $S1 ne "" or $NSEW_1 ne ""){

print<<"TABLETWENTYEIGHT"; 
              <tr>
                <td align="right" bgcolor="#EEEEEE"> &nbsp;&nbsp;&nbsp;&nbsp;
                  <font size=2><b>T1:</b></font>&nbsp; </td>
                <td> 
TABLETWENTYEIGHT
print("$T1");
print<<"TABLETWENTYNINE"; 
&nbsp;&nbsp;&nbsp;&nbsp; </td>
                <td align="right" bgcolor="#EEEEEE"> &nbsp;&nbsp;&nbsp;&nbsp;
                  <font size=2><b>R1:</b></font>&nbsp; </td>
                <td> 
TABLETWENTYNINE
print("$R1");
print<<"TABLETHIRTY"; 

&nbsp;&nbsp;&nbsp;&nbsp; </td>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>S1:</b></font>&nbsp;
                </td>
                <td> 
TABLETHIRTY

print("$S1");

print<<"TABLETHIRTYONE"; 
&nbsp;&nbsp;&nbsp;&nbsp; </td>
                <td align="right" bgcolor="#EEEEEE"> &nbsp;<font size=2><b>Quarter
                  Secs. 1:</b></font>&nbsp; </td>
                <td> 
TABLETHIRTYONE

print("$NSEW_1");
print<<"TABLETHIRTYTWO"; 
</td>
              </tr>
TABLETHIRTYTWO
	}
	if($T2 ne "" or $R2 ne "" or $S2 ne "" or $NSEW_2 ne ""){

print<<"TABLETHIRTYTHREE"; 
              <tr>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>T2:</b></font>&nbsp;
                </td>
                <td> 
TABLETHIRTYTHREE

print("$T2");

print<<"TABLETHIRTYFOUR"; 
</td>
                <td align="right" bgcolor="#EEEEEE"> &nbsp;&nbsp;&nbsp; <font size=2><b>R2:</b></font>&nbsp;
                </td>
                <td> 
TABLETHIRTYFOUR

print("$R2");

print<<"TABLETHIRTYFIVE"; 
</td>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>S2:</b></font>&nbsp;
                </td>
                <td> 
TABLETHIRTYFIVE

print("$S2");

print<<"TABLETHIRTYSIX"; 
</td>
                <td align="right" bgcolor="#EEEEEE"> &nbsp;<font size=2><b>Quarter
                  Secs. 2:</b></font>&nbsp; </td>
                <td> 
TABLETHIRTYSIX

print("$NSEW_2");

print<<"TABLETHIRTYSEVEN"; 
</td>
              </tr>
TABLETHIRTYSEVEN
	}
print<<"TABLETHIRTYEIGHT"; 
              <tr>
                <td>&nbsp; </td>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Lat:</b></font>&nbsp;
                </td>
                <td colspan=2> 
TABLETHIRTYEIGHT

print("$LAT");
print<<"TABLETHIRTYNINE"; 

</td>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>LatDec:</b></font>&nbsp;
                </td>
                <td colspan=2> 
TABLETHIRTYNINE
print("$LTDEC");

print<<"TABLEFORTY"; 
</td>
              </tr>
              <tr>
                <td>&nbsp; </td>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Long:</b></font>&nbsp;
                </td>
                <td colspan=2> 
TABLEFORTY

print("$LONGX");
print<<"TABLEFORTYONE"; 

</td>
                <td align="right" bgcolor="#EEEEEE"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                  <font size=2><b>LongDec:</b></font>&nbsp; </td>
                <td colspan=2> 
TABLEFORTYONE

print("$LGDEC");

print<<"TABLEFORTYTWO"; 
</td>
              </tr>
              <tr>
                <td colspan="7">&nbsp; </td>
              </tr>
              <tr>
                <td>&nbsp; </td>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Lat2:</b></font>&nbsp;
                </td>
                <td colspan=2> 
TABLEFORTYTWO

print("$LAT2");

print<<"TABLEFORTYTHREE"; 
</td>
                <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Long2:</b></font>&nbsp;
                </td>
                <td colspan="2"> 
TABLEFORTYTHREE



print("$LONG2");

print<<"TABLEFORTYFOUR"; 
</td>
              </tr>
            </table></td>
        </tr> 
TABLEFORTYFOUR
	if($ELEV ne "" or $MAPFILE ne ""){

print<<"TABLEFORTYFIVE"; 
        <tr>
          <td colspan=6>&nbsp; </td>
        </tr>
        <tr>
          <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Elev:</b></font>&nbsp;
          </td>
          <td> 
TABLEFORTYFIVE

print("$ELEV");

print<<"TABLEFORTYSIX"; 
</td>
          <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Map:</b></font>&nbsp;
          </td>
          <td> 
TABLEFORTYSIX

print("$MAPFILE");

print<<"TABLEFORTYSEVEN"; 
</td>
        </tr>
TABLEFORTYSEVEN
	}
}else{

print<<"TABLEFORTYEIGHT"; 
        <tr>
          <td colspan="4"> <br>
            *<em>more specific location information is undisclosed because of
            endangered/protected status.</em> </td>
        </tr>
TABLEFORTYEIGHT
}

print<<"TABLEFORTYNINE"; 
      </table>
      <br> </td>
  </tr>
TABLEFORTYNINE

if($HABITAT ne "" or $HABITAT_MISC ne "") { 
print<<"TABLEFIFTY"; 

  <tr>
    <td> <table border=0>
        <tr>
          <td align="right" valign="top" bgcolor="#EEEEEE"> <font size=2><b>Habitat:</b></font>&nbsp;
          </td>
          <td colspan=2> 
TABLEFIFTY

print("$HABITAT");

print<<"TABLEFIFTYONE"; 
</td>
        </tr>
        <tr>
          <td>&nbsp; </td>
        </tr>
        <tr>
          <td align="right" valign="top" bgcolor="#EEEEEE"> <font size=2><b>Text:</b></font>&nbsp;
          </td>
          <td colspan=2> 
TABLEFIFTYONE

print("$HABITAT_MISC");
print<<"TABLEFIFTYTWO"; 

</td>
        </tr>
      </table>
      <br> </td>
    <td>&nbsp;</td>
  </tr>
TABLEFIFTYTWO
	}
print<<"TABLEFIFTYTHREE"; 
  <tr>
    <td> <table border="0">
        <tr>
          <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Collection No.:</b></font>
          </td>
          <td> 
TABLEFIFTYTHREE

print("$COLLNO1");

print<<"TABLEFIFTYFOUR"; 
&nbsp;&nbsp;&nbsp;&nbsp; </td>
          <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Collector 1:</b></font>
          </td>
          <td> 
TABLEFIFTYFOUR

print("$COLL1NAME");

print<<"TABLEFIFTYFIVE"; 
</td>
        </tr>
        <tr>
          <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Date:</b></font>
          </td>
          <td> 
TABLEFIFTYFIVE

#get the time out of the $COLLDATE string before printing, nobody cares what time it was:
$COLLDATE=~s/00:00:00//g;
print("$COLLDATE");

print<<"TABLEFIFTYSIX"; 
&nbsp;&nbsp;&nbsp;&nbsp; </td>
          <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Collector 2:</b></font>
          </td>
          <td> 
TABLEFIFTYSIX


print("$COLL2NAME");

print<<"TABLEFIFTYSEVEN"; 
</td>
        </tr>
        <tr>
          <td colspan=2>&nbsp; </td>
          <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Collector 3:</b></font>
          </td>
          <td> 
TABLEFIFTYSEVEN

print("$COLL3NAME");

print<<"TABLEFIFTYEIGHT"; 
</td>
        </tr>
      </table>
      <br> </td>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td> <table border="0">
        <tr>
          <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Annotator:</b></font>
          </td>
          <td colspan=2> 
TABLEFIFTYEIGHT

#The ANNCODE from the database table is something like 'HJN1' which might 
# mean ' Haas, J.N. | University of Basel; Najas' corresponding to the 
# ANNLKUP table's 'WHOLENAME' and 'BIO' fields.  Therefore, we need to run 
# a quick dblookup to find this info so that we can print it for the user: 
#print($ANNCODE);
#print(TOM-getAnnName($ANNCODE));
	my $sthtwo = $dbh->prepare ("SELECT * FROM ANNLKUP WHERE ANNCODE = '$ANNCODE'");
	$sthtwo->execute();
 	while (my ($ANNCODETWO, $WHOLENAME, $BIO, $ANNLKUP_id) = $sthtwo->fetchrow_array ()){
		print("$WHOLENAME");
		last;
	}


print<<"TABLEFIFTYNINE"; 
</td>
        </tr>
        <tr>
          <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Date:</b></font>
          </td>
          <td colspan="2"> 
TABLEFIFTYNINE

print("$ANNDATE");
print<<"TABLESIXTY"; 

</td>
        </tr>
        <tr>
          <td align="right" bgcolor="#EEEEEE"> <font size=2><b>Type:</b></font>
          </td>
          <td colspan="2"> 
TABLESIXTY

#print("TOM-maketypelookup($TYPE)");
print("$TYPE");

print<<"TABLESIXTYONE"; 
</td>
        </tr>
      </table></td>
    <td>&nbsp;</td>
  </tr>
</table>


TABLESIXTYONE

if($LTDECgmapGlobal=~/\d\d/) {
	if($LGDECgmapGlobal=~/\d\d/) {
		print("<BR>This specimen was collected here:<BR>\n");
		print("<div id=\"map\" style=\"width: 600px; height: 300px\"></div>\n");
	}
}






















# 		print $cgi->p("ACCESSION: $ACCESSION ");
#		print $cgi->p("  TYPE: $TYPE ");
#		print $cgi->p("  COLLDATE: $COLLDATE ");
#		print $cgi->p("  FLOWER: $FLOWER ");
#		print $cgi->p("  FRUIT: $FRUIT ");
#		print $cgi->p("  STERILE: $STERILE ");
#		print $cgi->p("  OBJTYPE: $OBJTYPE ");
#		print $cgi->p("  INST: $INST ");
#		print $cgi->p("  ANNCODE: $ANNCODE ");
#		print $cgi->p("  ANNDATE: $ANNDATE ");
#		print $cgi->p("  ANNSOURCE: $ANNSOURCE ");
#		print $cgi->p("  CITY: $CITY ");
#		print $cgi->p("  SITENO: $SITENO ");
#		print $cgi->p("  CITYTYPE: $CITYTYPE ");
#		print $cgi->p("  COLL2NAME: $COLL2NAME ");
#		print $cgi->p("  COLL3NAME: $COLL3NAME ");
#		print $cgi->p("  COLL1NAME: $COLL1NAME ");
#		print $cgi->p("  COLLNO1: $COLLNO1 ");
#		print $cgi->p("  COLLEVENT: $COLLEVENT ");
#		print $cgi->p("  TAXCD: $TAXCD ");
#		print $cgi->p("  CFS: $CFS ");
#		print $cgi->p("  CFV: $CFV ");
#		print $cgi->p("  CFVariety: $CFVariety ");
#		print $cgi->p("  HABITAT_MISC: $HABITAT_MISC ");
#		print $cgi->p("  HABITAT: $HABITAT ");
#		print $cgi->p("  LONGX: $LONGX ");
#		print $cgi->p("  LAT: $LAT ");
#		print $cgi->p("  ELEV: $ELEV ");
#		print $cgi->p("  LLGENER: $LLGENER ");
#		print $cgi->p("  LONG2: $LONG2 ");
#		print $cgi->p("  LAT2: $LAT2 ");
#		print $cgi->p("  LTDEC: $LTDEC ");
#		print $cgi->p("  LGDEC: $LGDEC ");
#		print $cgi->p("  NOWLOC: $NOWLOC ");
#		print $cgi->p("  LOAN: $LOAN ");
#		print $cgi->p("  PAGES: $PAGES ");
#		print $cgi->p("  ORIGCD: $ORIGCD ");
#		print $cgi->p("  PUBCD: $PUBCD ");
#		print $cgi->p("  LITCIT: $LITCIT ");
#		print $cgi->p("  PUBDATE: $PUBDATE ");
#		print $cgi->p("  PUBDATEA: $PUBDATEA ");
#		print $cgi->p("  VERPERS: $VERPERS ");
#		print $cgi->p("  VERDATE: $VERDATE ");
#		print $cgi->p("  EX: $EX ");
#		print $cgi->p("  ARTICLE: $ARTICLE ");
#		print $cgi->p("  PREC: $PREC ");
#		print $cgi->p("  STATEL: $STATEL ");
#		print $cgi->p("  COUNTY: $COUNTY ");
#		print $cgi->p("  COUNTRY: $COUNTRY ");
#		print $cgi->p("  T1: $T1 ");
#		print $cgi->p("  R1: $R1 ");
#		print $cgi->p("  S1: $S1 ");
#		print $cgi->p("  NSEW_1: $NSEW_1 ");
#		print $cgi->p("  TRSGENER: $TRSGENER ");
#		print $cgi->p("  T2: $T2 ");
#		print $cgi->p("  R2: $R2 ");
#		print $cgi->p("  S2: $S2 ");
#		print $cgi->p("  NSEW_2: $NSEW_2 ");
#		print $cgi->p("  PLACE: $PLACE ");
#		print $cgi->p("  scan: $scan ");
#		print $cgi->p("  MAPFILE: $MAPFILE ");
#		print $cgi->p("  username: $username ");
#		print $cgi->p("  date_time: $date_time ");
#		print $cgi->p("  DTRS: $DTRS ");
#		#not used anymore:
#		#print $cgi->p("  specimen_id: $specimen_id");





	#END while
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
        while (my ($Taxcd, $Syncd, $family_code, $genus, $species, $authority, $subsp, $variety,
$forma, $subsp_auth, $var_auth, $forma_auth, $sub_family, $tribe, $common, $Wisc_found, $ssp, $var, $f, $hybrids, $status_code, $hide, $USDA, $COFC, $WETINDICAT, $FAM_NAME, $FAMILY, $GC, $FAMILY_COMMON, $SYNWisc_found, $SYNS_STATUS, $SYNV_STATUS, $SYNF_STATUS, $SYNHYBRIDS_STATUS, $SYNW_STATUS, $speciesweb_Taxcd, $Status, $Photo, $Photographer, $Thumbmaps, $Accgenus, $SORTOR, $Hand, $growth_habit_bck, $blooming_dt_bck, $origin_bck, $Thumbphoto, $date_time, $growth_habit, $blooming_dt, $origin, $Taxa, $spdetail_id ) = $sth->fetchrow_array ()){
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
