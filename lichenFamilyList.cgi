#!/usr/bin/perl
# lichenFamilyList.cgi -wisflora Family listing 
#This script generates an HTML listing of unique family names of species found in WI

use strict;
use warnings;
use CGI;
use DBI;

my $title = "lichenFamilyList.cgi";
my $cgi = new CGI();
print $cgi->header(); 
print $cgi->start_html(-title => $title, -bgcolor => "white");
my $dsn = "DBI:mysql:host=localhost;database=lichenone";
my $dbh = DBI->connect($dsn, "apache", "apachePASS") or die "cantconnect $!";
	{ # begin scope
	#Start generating HTML header:
	my $h = <<"HEADER";
	<table width="100%" border="0" bgcolor="#EEEEEE">
	  <tr bgcolor="#E7E7B6">
	    <td width="100%" bgcolor="#E7E7B6"><font color="#990000"><font size=+3>W</font><b><font size=+1>ISCONSIN </font></b><font size=+3>B</font>
	<b><font size=+1>OTANICAL </font></b><font size=+3>I</font><b><font size=+1>NFORMATION </font></b><font size=+3>S</font><b><font size=+1>YSTEM
	</font></b></font></td>
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
HEADER
#it would be nice to indent the previous (and this line), but it needs to be flush right.
	#printout HTML header:
	print("$h");

	print("<h1>List of Families</h1>");
	print("<font size=-1>");
	print("To Search - Click on Alphabet index below. (<a href=\"http://www.colby.edu/info.tech/BI211/PlantFamilyID.html\" Target=\"anyname\">Key to Families -Colby College</a>)</font>");


	
	print("<br><font face=\"COURIER\"><font size=+1>");
	print("<a href=\"#A\">A</a>&nbsp<a href=\"#B\">B</a>&nbsp<a href=\"#C\">C</a>&nbsp<a href=\"#D\">D</a>&nbsp<a href=\"#E\">E</a>&nbsp<a href=\"#F\">F</a>&nbsp<a href=\"#G\">G</a>&nbsp<a href=\"#H\">H</a>&nbsp<a href=\"#I\">I</a>&nbsp<a href=\"#J\">J</a>&nbsp<a href=\"#K\">K</a>&nbsp<a href=\"#L\">L</a>&nbsp<a href=\"#M\">M</a>&nbsp<a href=\"#N\">N</a>&nbsp<a href=\"#O\">O</a>&nbsp<a href=\"#P\">P</a>&nbsp<a href=\"#Q\">Q</a>&nbsp<a href=\"#R\">R</a>&nbsp<a href=\"#S\">S</a>&nbsp<a href=\"#T\">T</a>&nbsp<a href=\"#U\">U</a>&nbsp<a href=\"#V\">V</a>&nbsp<a href=\"#W\">W</a>&nbsp<a href=\"#X\">X</a>&nbsp<a href=\"#Y\">Y</a>&nbsp<a href=\"#Z\">Z</a></font></font>");

	# _PRINT_COLORED_CD_TABLE_
	my $sth = $dbh->prepare ("SELECT DISTINCT Family FROM spdetail WHERE syncd = '.' AND Wisc_Found = 'W' ORDER BY Family");
	$sth->execute ();
	my $bgcolor = "white";   # row-color variable
	my @rows = ();
	my $turnAnchoringBackOn = 1;
	my $anchor = "";
	#al stands for anchorletter 
	my $al = "";
	#af stands for anchorflag
	my $af = "";

#	push (@rows, $cgi->Tr (
#	              $cgi->th ({-bgcolor => $bgcolor}, "List of Families"),
#	            ));
	while (my ($Family) = $sth->fetchrow_array ())
	{
	  # toggle the row-color variable...or not:
	  $bgcolor = ($bgcolor eq "silver" ? "white" : "silver");
		if($Family=~/^A/){ if($af=~/A/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"A\"></a>"; $al = "A"; $af = "A";} }
		if($Family=~/^B/){ if($af=~/B/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"B\"></a>"; $al = "B"; $af = "B";} }
		if($Family=~/^C/){ if($af=~/C/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"C\"></a>"; $al = "C"; $af = "C";} }
		if($Family=~/^D/){ if($af=~/D/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"D\"></a>"; $al = "D"; $af = "D";} }
		if($Family=~/^E/){ if($af=~/E/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"E\"></a>"; $al = "E"; $af = "E";} }
		if($Family=~/^F/){ if($af=~/F/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"F\"></a>"; $al = "F"; $af = "F";} }
		if($Family=~/^G/){ if($af=~/G/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"G\"></a>"; $al = "G"; $af = "G";} }
		if($Family=~/^H/){ if($af=~/H/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"H\"></a>"; $al = "H"; $af = "H";} }
		if($Family=~/^I/){ if($af=~/I/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"I\"></a>"; $al = "I"; $af = "I";} }
		if($Family=~/^J/){ if($af=~/J/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"J\"></a>"; $al = "J"; $af = "J";} }
		if($Family=~/^K/){ if($af=~/K/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"K\"></a>"; $al = "K"; $af = "K";} }
		if($Family=~/^L/){ if($af=~/L/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"L\"></a>"; $al = "L"; $af = "L";} }
		if($Family=~/^M/){ if($af=~/M/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"M\"></a>"; $al = "M"; $af = "M";} }
		if($Family=~/^N/){ if($af=~/N/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"N\"></a>"; $al = "N"; $af = "N";} }
		if($Family=~/^O/){ if($af=~/O/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"O\"></a>"; $al = "O"; $af = "O";} }
		if($Family=~/^P/){ if($af=~/P/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"P\"></a>"; $al = "P"; $af = "P";} }
		if($Family=~/^Q/){ if($af=~/Q/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"Q\"></a>"; $al = "Q"; $af = "Q";} }
		if($Family=~/^R/){ if($af=~/R/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"R\"></a>"; $al = "R"; $af = "R";} }
		if($Family=~/^S/){ if($af=~/S/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"S\"></a>"; $al = "S"; $af = "S";} }
		if($Family=~/^T/){ if($af=~/T/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"T\"></a>"; $al = "T"; $af = "T";} }
		if($Family=~/^U/){ if($af=~/U/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"U\"></a>"; $al = "U"; $af = "U";} }
		if($Family=~/^V/){ if($af=~/V/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"V\"></a>"; $al = "V"; $af = "V";} }
		if($Family=~/^W/){ if($af=~/W/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"W\"></a>"; $al = "W"; $af = "W";} }
		if($Family=~/^X/){ if($af=~/X/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"X\"></a>"; $al = "X"; $af = "X";} }
		if($Family=~/^Y/){ if($af=~/Y/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"Y\"></a>"; $al = "Y"; $af = "Y";} }
		if($Family=~/^Z/){ if($af=~/Z/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"Z\"></a>"; $al = "Z"; $af = "Z";} }

	#add an empty table row if we are at a new letter:
	if($al=~/[A-Z]/){ 
	  push (@rows, $cgi->Tr (
	               $cgi->td({-bgcolor => "white", -width => 95 }, "&nbsp;").$cgi->td({-bgcolor => "white"}, "&nbsp;")
	          ));
	}
	  push (@rows, $cgi->Tr (
	               $cgi->td({-bgcolor => "silver", -width => 95 }, "<font face=\"Times New Roman\"><font color=\"#800000\"><font size=+1>$al</font></font></font>").$cgi->td({-bgcolor => "white"}, $cgi->a({href=>"/cgi-bin/SearchResults.cgi?Family=$Family"}, "$Family").$anchor)
	          ));
		$al = "";
	}
	print $cgi->table({-border => "0", -cellspacing => 0, -bordercolor => "silver"}, @rows);
	# _PRINT_COLORED_CD_TABLE_
	#Start generating HTML footer:
	my $foot = <<"FOOT";
	<table width="100%" border="0">
	  <tr bgcolor="#EEEEEE">
	    <td align="center" width="25%">
	      <p><strong>Menu:</strong> <font size=2><a href="/herbarium/"><b>Herbarium Home</b></a></font> </p></td>
	    <td align="center" width="25%"> <font size="2"><a href="/wisflora/"><b>WISFLORA: Vascular Plant Species</b></a></font></td>
	    <td align="center" width="25%"> <font size="2"><a href="/herb/search.html"><b>Vascular Plant Taxon Search</b></a></font> </td>
	    <td align="center" width="25%"> <font size="2"><a href="/herb/specimenSearch.html"><b>Search Specimen Database</b></a></font> </td>
	  </tr>
	</table>
FOOT
#it would be nice to indent the previous (and this line), but it needs to be flush right.
	#printout HTML footer:
	print("$foot");
	
} # end scope

$dbh->disconnect ();
print $cgi->end_html();
exit (0);

