#!/usr/bin/perl
# GenusList.cgi -wisflora Genus listing 

use strict;
use warnings;
use CGI;
use DBI;

my $title = "GenusList.cgi";
my $cgi = new CGI();
print $cgi->header(); 
print $cgi->start_html(-title => $title, -bgcolor => "white");

my $dsn = "DBI:mysql:host=localhost;database=herbfortynine";
my $dbh = DBI->connect($dsn, "apache", "apachePASS") or die "cantconnect $!";
{ # begin scope






print <<HEADER;
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





        print("<h1>List of Genera</h1>");
        print("<font size=-1>");
        print("To Search - Click on Alphabet index below. ");



        print("<br><font face=\"COURIER\"><font size=+1>");
        print("<a href=\"#A\">A</a>&nbsp<a href=\"#B\">B</a>&nbsp<a href=\"#C\">C</a>&nbsp<a href=\"#D\">D</a>&nbsp<a href=\"#E\">E</a>&nbsp<a href=\"#F\">F</a>&nbsp<a href=\"#G\">G</a>&nbsp<a href=\"#H\">H</a>&nbsp<a href=\"#I\">I</a>&nbsp<a href=\"#J\">J</a>&nbsp<a href=\"#K\">K</a>&nbsp<a href=\"#L\">L</a>&nbsp<a href=\"#M\">M</a>&nbsp<a href=\"#N\">N</a>&nbsp<a href=\"#O\">O</a>&nbsp<a href=\"#P\">P</a>&nbsp<a href=\"#Q\">Q</a>&nbsp<a href=\"#R\">R</a>&nbsp<a href=\"#S\">S</a>&nbsp<a href=\"#T\">T</a>&nbsp<a href=\"#U\">U</a>&nbsp<a href=\"#V\">V</a>&nbsp<a href=\"#W\">W</a>&nbsp<a href=\"#X\">X</a>&nbsp<a href=\"#Y\">Y</a>&nbsp<a href=\"#Z\">Z</a></font></font>");






# _PRINT_COLORED_CD_TABLE_
my $sth = $dbh->prepare ("SELECT DISTINCT Genus FROM spdetail WHERE syncd = '.' AND Wisc_Found = 'W' ORDER BY Genus");
$sth->execute ();
my $bgcolor = "white";   # row-color variable

my $anchor = "";
#al stands for anchorletter 
my $al = "";
#af stands for anchorflag
my $af = "";


my @rows = ();
while (my ($Genus) = $sth->fetchrow_array ())
{

   if($Genus=~/^A/){ if($af=~/A/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"A\"></a>"; $al = "A"; $af = "A";} }
   if($Genus=~/^B/){ if($af=~/B/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"B\"></a>"; $al = "B"; $af = "B";} }
   if($Genus=~/^C/){ if($af=~/C/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"C\"></a>"; $al = "C"; $af = "C";} }
   if($Genus=~/^D/){ if($af=~/D/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"D\"></a>"; $al = "D"; $af = "D";} }
   if($Genus=~/^E/){ if($af=~/E/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"E\"></a>"; $al = "E"; $af = "E";} }
   if($Genus=~/^F/){ if($af=~/F/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"F\"></a>"; $al = "F"; $af = "F";} }
   if($Genus=~/^G/){ if($af=~/G/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"G\"></a>"; $al = "G"; $af = "G";} }
   if($Genus=~/^H/){ if($af=~/H/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"H\"></a>"; $al = "H"; $af = "H";} }
   if($Genus=~/^I/){ if($af=~/I/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"I\"></a>"; $al = "I"; $af = "I";} }
   if($Genus=~/^J/){ if($af=~/J/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"J\"></a>"; $al = "J"; $af = "J";} }
   if($Genus=~/^K/){ if($af=~/K/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"K\"></a>"; $al = "K"; $af = "K";} }
   if($Genus=~/^L/){ if($af=~/L/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"L\"></a>"; $al = "L"; $af = "L";} }
   if($Genus=~/^M/){ if($af=~/M/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"M\"></a>"; $al = "M"; $af = "M";} }
   if($Genus=~/^N/){ if($af=~/N/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"N\"></a>"; $al = "N"; $af = "N";} }
   if($Genus=~/^O/){ if($af=~/O/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"O\"></a>"; $al = "O"; $af = "O";} }
   if($Genus=~/^P/){ if($af=~/P/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"P\"></a>"; $al = "P"; $af = "P";} }
   if($Genus=~/^Q/){ if($af=~/Q/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"Q\"></a>"; $al = "Q"; $af = "Q";} }
   if($Genus=~/^R/){ if($af=~/R/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"R\"></a>"; $al = "R"; $af = "R";} }
   if($Genus=~/^S/){ if($af=~/S/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"S\"></a>"; $al = "S"; $af = "S";} }
   if($Genus=~/^T/){ if($af=~/T/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"T\"></a>"; $al = "T"; $af = "T";} }
   if($Genus=~/^U/){ if($af=~/U/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"U\"></a>"; $al = "U"; $af = "U";} }
   if($Genus=~/^V/){ if($af=~/V/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"V\"></a>"; $al = "V"; $af = "V";} }
   if($Genus=~/^W/){ if($af=~/W/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"W\"></a>"; $al = "W"; $af = "W";} }
   if($Genus=~/^X/){ if($af=~/X/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"X\"></a>"; $al = "X"; $af = "X";} }
   if($Genus=~/^Y/){ if($af=~/Y/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"Y\"></a>"; $al = "Y"; $af = "Y";} }
   if($Genus=~/^Z/){ if($af=~/Z/) { $al = "";  $anchor = "" ;}else{ $anchor = "<a name=\"Z\"></a>"; $al = "Z"; $af = "Z";} }

#add an empty table row if we are at a new letter:
   if($al=~/[A-Z]/){ 
	push (@rows, $cgi->Tr (
	$cgi->td({-bgcolor => "white", -width => 95 }, "&nbsp;").$cgi->td({-bgcolor => "white"}, "&nbsp;")
	));
   }
        push (@rows, $cgi->Tr (
        $cgi->td({-bgcolor => "silver", -width => 95 }, "<font face=\"Times New Roman\"><font color=\"#800000\"><font size=+1>$al</font></font></font>").$cgi->td({-bgcolor => "white"}, $cgi->a({href=>"/cgi-bin/SearchResults.cgi?Genus=$Genus"}, "$Genus").$anchor)
        ));
        $al = "";
}
print $cgi->table({-border => "0", -cellspacing => 0, -bordercolor => "silver" }, @rows);
# _PRINT_COLORED_CD_TABLE_
} # end scope
$dbh->disconnect ();







print <<FOOTER;
print $cgi->br();
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






print $cgi->end_html();
exit (0);

