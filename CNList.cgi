#!/usr/bin/perl
# CNList.cgi -wisflora Common Name listing 

use strict;
use warnings;
use CGI;
use DBI;

my $title = "CNList.cgi";
my $cgi = new CGI();
print $cgi->header(); 
print $cgi->start_html(-title => $title, -bgcolor => "white");
my $dsn = "DBI:mysql:host=localhost;database=herbfortynine";
my $dbh = DBI->connect($dsn, "apache", "apachePASS") or die "cantconnect $!";
{ # begin scope
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
print("$h");

        print("<h1>List of Common Names</h1>");
        print("<font size=-1>");
        print("To Search - Click on Alphabet index below. </font>");

        
        print("<br><font face=\"COURIER\"><font size=+1>");
        print("<a href=\"#A\">A</a>&nbsp<a href=\"#B\">B</a>&nbsp<a href=\"#C\">C</a>&nbsp<a href=\"#D\">D</a>&nbsp<a href=\"#E\">E</a>&nbsp<a href=\"#F\">F</a>&nbsp<a href=\"#G\">G</a>&nbsp<a href=\"#H\">H</a>&nbsp<a href=\"#I\">I</a>&nbsp<a href=\"#J\">J</a>&nbsp<a href=\"#K\">K</a>&nbsp<a href=\"#L\">L</a>&nbsp<a href=\"#M\">M</a>&nbsp<a href=\"#N\">N</a>&nbsp<a href=\"#O\">O</a>&nbsp<a href=\"#P\">P</a>&nbsp<a href=\"#Q\">Q</a>&nbsp<a href=\"#R\">R</a>&nbsp<a href=\"#S\">S</a>&nbsp<a href=\"#T\">T</a>&nbsp<a href=\"#U\">U</a>&nbsp<a href=\"#V\">V</a>&nbsp<a href=\"#W\">W</a>&nbsp<a href=\"#X\">X</a>&nbsp<a href=\"#Y\">Y</a>&nbsp<a href=\"#Z\">Z</a></font></font>");




# _PRINT_COLORED_CD_TABLE_
my $sth = $dbh->prepare ("SELECT DISTINCT common FROM t_vascular_common_names WHERE common IS NOT NULL AND WiscFound = 'W' ORDER BY common");
$sth->execute ();
my $bgcolor = "white";   # row-color variable

my $anchor = "";
#al stands for anchorletter 
my $al = "";
#af stands for anchorflag
my $af = "";


my @rows = ();
#This label "FETCH:" will allow us to ditch bad records and get a new one instead:
FETCH: while (my ($Common) = $sth->fetchrow_array ())
{
  #bad records (in this case) are recs that begin with = or ', next over bad recs
	  if($Common=~/^[=,']/){
	next FETCH;
  }
  # toggle the row-color variable ORNOT
  #$bgcolor = ($bgcolor eq "silver" ? "white" : "silver");

                if($Common=~/^A/i){ if($af=~/A/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"A\"></a>"; $al = "A"; $af = "A";} }
                if($Common=~/^B/i){ if($af=~/B/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"B\"></a>"; $al = "B"; $af = "B";} }
                if($Common=~/^C/i){ if($af=~/C/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"C\"></a>"; $al = "C"; $af = "C";} }
                if($Common=~/^D/i){ if($af=~/D/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"D\"></a>"; $al = "D"; $af = "D";} }
                if($Common=~/^E/i){ if($af=~/E/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"E\"></a>"; $al = "E"; $af = "E";} }
                if($Common=~/^F/i){ if($af=~/F/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"F\"></a>"; $al = "F"; $af = "F";} }
                if($Common=~/^G/i){ if($af=~/G/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"G\"></a>"; $al = "G"; $af = "G";} }
                if($Common=~/^H/i){ if($af=~/H/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"H\"></a>"; $al = "H"; $af = "H";} }
                if($Common=~/^I/i){ if($af=~/I/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"I\"></a>"; $al = "I"; $af = "I";} }
                if($Common=~/^J/i){ if($af=~/J/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"J\"></a>"; $al = "J"; $af = "J";} }
                if($Common=~/^K/i){ if($af=~/K/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"K\"></a>"; $al = "K"; $af = "K";} }
                if($Common=~/^L/i){ if($af=~/L/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"L\"></a>"; $al = "L"; $af = "L";} }
                if($Common=~/^M/i){ if($af=~/M/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"M\"></a>"; $al = "M"; $af = "M";} }
                if($Common=~/^N/i){ if($af=~/N/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"N\"></a>"; $al = "N"; $af = "N";} }
                if($Common=~/^O/i){ if($af=~/O/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"O\"></a>"; $al = "O"; $af = "O";} }
                if($Common=~/^P/i){ if($af=~/P/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"P\"></a>"; $al = "P"; $af = "P";} }
                if($Common=~/^Q/i){ if($af=~/Q/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"Q\"></a>"; $al = "Q"; $af = "Q";} }
                if($Common=~/^R/i){ if($af=~/R/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"R\"></a>"; $al = "R"; $af = "R";} }
                if($Common=~/^S/i){ if($af=~/S/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"S\"></a>"; $al = "S"; $af = "S";} }
                if($Common=~/^T/i){ if($af=~/T/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"T\"></a>"; $al = "T"; $af = "T";} }
                if($Common=~/^U/i){ if($af=~/U/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"U\"></a>"; $al = "U"; $af = "U";} }
                if($Common=~/^V/i){ if($af=~/V/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"V\"></a>"; $al = "V"; $af = "V";} }
                if($Common=~/^W/i){ if($af=~/W/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"W\"></a>"; $al = "W"; $af = "W";} }
                if($Common=~/^X/i){ if($af=~/X/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"X\"></a>"; $al = "X"; $af = "X";} }
                if($Common=~/^Y/i){ if($af=~/Y/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"Y\"></a>"; $al = "Y"; $af = "Y";} }
                if($Common=~/^Z/i){ if($af=~/Z/i) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"Z\"></a>"; $al = "Z"; $af = "Z";} }

        #add an empty table row if we are at a new letter:
  if($al=~/[A-Z]/){ 
  	push (@rows, $cgi->Tr (
  		$cgi->td({-bgcolor => "white", -width => 95 }, "&nbsp;").$cgi->td({-bgcolor => "white"}, "&nbsp;")
  	));
  }
  push (@rows, $cgi->Tr (
                       $cgi->td({-bgcolor => "silver", -width => 95 }, "<font face=\"Times New Roman\"><font color=\"#800000\"><font size=+1>$al</font></font></font>").$cgi->td({-bgcolor => "white"}, $cgi->a({href=>"/cgi-bin/SearchResults.cgi?Common=$Common"}, "$Common").$anchor)
                  ));
                $al = "";

}
print $cgi->table({-border => "0", -cellspacing => 0, -bordercolor => "silver" }, @rows);
# _PRINT_COLORED_CD_TABLE_
} # end scope
$dbh->disconnect ();
print $cgi->end_html();
exit (0);

