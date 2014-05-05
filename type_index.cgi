<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<HEAD>
	<TITLE>Type Scans : Index Page</TITLE>
</HEAD>

<!--#include virtual="/wisflora/dbman/includes/shared//dbconnectVIEW.asp"-->
<!--#include virtual="/wisflora/dbman/includes/shared/incdbtools.asp"-->

<!--#include virtual="/wisflora/dbman/includes/shared/incannotator.asp"-->
<!--#include virtual="/wisflora/dbman/includes/shared/inccollevent.asp"-->

<!--#include virtual="/wisflora/specimen/includes/increstricted.asp"-->

<!--#include virtual="/wisflora/specimen/includes/spec_pub_head.asp" -->
<!--#include virtual="/wisflora/specimen/includes/spec_pub_menu.asp" -->

<body>
<div align="center"> <font color="#000000" size="5" face="Arial, Helvetica, sans-serif">
	<strong><br>Type Specimen Scans</strong></font><br>
  <font size="3" color="#000000"><strong>Wisconsin and non-Wisconsin Specimens<br>
  </strong></font><FONT face="PrimaSans BT,Verdana,sans-serif"><SPAN xmlns="http://www.w3.org/TR/REC-html40" 
xmlns:st1="urn:schemas-microsoft-com:office:smarttags" 
xmlns:w="urn:schemas-microsoft-com:office:word" 
xmlns:o="urn:schemas-microsoft-com:office:office"><SPAN lang=EN-US vlink="purple" link="blue"><STRONG><B><FONT face="Times New Roman" color=black size=3><SPAN 
style="FONT-SIZE: 12pt; COLOR: black">(Approximately 5 % of total estimated types)</SPAN></FONT></B></STRONG></SPAN></SPAN></FONT><font size="3" color="#000000"><strong>  </strong></font></div>
	<br><br><%
	call ffWriteODBCError()
	
	response.write "<div align='center'>"						
									dim reason
									reason = request.querystring("page")
									select case reason
									case 1
									response.write("<a href=type_index.asp> A-C </a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;D-I&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;<a href=type_index.asp?page=2>J-P</a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;<a href=type_index.asp?page=3> Q-V </a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;<a href=type_index.asp?page=4> W-Z </a>&nbsp;<br>")
'									set j=0
									response.write("&nbsp;&nbsp;&nbsp;")
									For intIndex = 68 to 73
									strAlpha=chr(intIndex) %>
									<a href="#<%=strAlpha%>"> 
									<%=strAlpha%> </a>&nbsp; 
									<% next %>
									<%
									For intIndex = 68 to 73
									strAlpha = chr(intIndex)
 									i=0 %>
										<a NAME="<%=strAlpha%>"></a>
										
										<table width="80%" border="1" cellspacing="2" cellpadding="2" frame="border">
										<tr bgcolor="#999999">
										<td><font color="#800000" size="+1" face="Times New Roman"><%=strAlpha%></font></td>
										</tr><tr><td width='20%' height='20' VALIGN=TOP> 
										
									<%
									'Increase table width so there is no word wrapping.
									'Changes for query:  add "ORDER BY spdetail.TAXA, specimen.ACCESSION"  --> We may have to live with the fact that
									'all hybrids will be at the bottom of the list; If this fact is noted at the top of the page for the users then it shouldn't be a big deal.
									'After select queries for each letter, check of EOF, and if so then don't display Lettered box at all.
									'sadam, 01.07	
									'MySQL = "SELECT specimen.ACCESSION,spdetail.TAXA FROM specimen, spdetail WHERE ((spdetail.taxcd = specimen.taxcd) AND (specimen.TYPE <> ' ') AND (spdetail.TAXA like '"&chr(intIndex)&"%')) ORDER BY specimen.Accession"
									MySQL = "SELECT     specimen.ACCESSION, spdetail.Taxa FROM specimen INNER JOIN spdetail ON specimen.TAXCD = spdetail.Taxcd WHERE (spdetail.syncd = '.' AND specimen.TYPE <> ' ' AND specimen.scan='1') AND (spdetail.Taxa LIKE '"&chr(intIndex)&"%') ORDER BY spdetail.TAXA, specimen.ACCESSION" 
									
									Set RS = MyConn.Execute(MySQL)
									while not RS.EOF 
									response.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='../specimen/scripts/specimen.asp?Accession="&RS("ACCESSION")&"' target=_blank>")
									response.write(RS("TAXA"))
									response.write("</a> - <font size=-1 color='#666666'>" & RS("ACCESSION") & "</font><br>")
									RS.movenext
									wend
									%></td></tr>					
									<tr>
									<% if strAlpha <>"D" then
									response.write("&nbsp; &nbsp; &nbsp;<a href='#top'> <font color='red'> TOP </font></a>")
									end if
									%></tr>
											</table>
									<br>
									<% next 
									case 2
									response.write("<a href=type_index.asp> A-C </a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;<a href=type_index.asp?page=1> D-I </a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;J-P&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;<a href=type_index.asp?page=3> Q-V </a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;<a href=type_index.asp?page=4> W-Z </a>&nbsp;<br>")
									response.write("&nbsp;&nbsp;&nbsp;")
									For intIndex = 74 to 80
									strAlpha=chr(intIndex) %>
									<a href="#<%=strAlpha%>"> 
									<%=strAlpha%> </a>&nbsp; 
									<% next %>
									<%
									For intIndex = 74 to 80
									strAlpha = chr(intIndex)
 									i=0 %>
										<a NAME="<%=strAlpha%>"></a>
										
										<table width="80%" border="1" cellspacing="2" cellpadding="2" frame="border">
										<tr bgcolor="#999999">
										<td><font color="#800000" size="+1" face="Times New Roman"><%=strAlpha%></font></td>
										</tr><tr><td width='20%' height='20' VALIGN=TOP> 
										
									<%	
									'MySQL = "SELECT specimen.ACCESSION,spdetail.TAXA FROM specimen, spdetail WHERE ((spdetail.taxcd = specimen.taxcd) AND (specimen.TYPE <> ' ') AND (spdetail.TAXA like '"&chr(intIndex)&"%')) ORDER BY specimen.Accession"
									MySQL = "SELECT specimen.ACCESSION, spdetail.Taxa FROM specimen INNER JOIN spdetail ON specimen.TAXCD = spdetail.Taxcd WHERE (spdetail.syncd = '.' AND specimen.TYPE <> ' ' AND specimen.scan='1') AND (spdetail.Taxa LIKE '"&chr(intIndex)&"%') ORDER BY spdetail.TAXA, specimen.ACCESSION" 
									
									Set RS = MyConn.Execute(MySQL)
									while not RS.EOF 
									response.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='../specimen/scripts/specimen.asp?Accession="&RS("ACCESSION")&"' target=_blank>")
									response.write(RS("TAXA"))
									response.write("</a> - <font size=-1 color='#666666'>" & RS("ACCESSION") & "</font><br>")
									RS.movenext
									wend
									%></td></tr>					
									<tr>
									<% if strAlpha <>"J" then
									response.write("&nbsp; &nbsp; &nbsp;<a href='#top'> <font color='red'> TOP </font></a>")
									end if
									%></tr>
											</table>
									<br>
									<% next 
									case 3
									response.write("<a href=type_index.asp> A-C </a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;<a href=type_index.asp?page=1> D-I </a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;<a href=type_index.asp?page=2>J-P</a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;Q-V&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;<a href=type_index.asp?page=4> W-Z </a>&nbsp;<br>")
									response.write("&nbsp;&nbsp;&nbsp;")
									For intIndex = 81 to 86
									strAlpha=chr(intIndex) %>
									<a href="#<%=strAlpha%>"> 
									<%=strAlpha%> </a>&nbsp; 
									<% next %>
									<%
									For intIndex = 81 to 86
									strAlpha = chr(intIndex)
 									i=0 %>
										<a NAME="<%=strAlpha%>"></a>
										
										<table width="80%" border="1" cellspacing="2" cellpadding="2" frame="border">
										<tr bgcolor="#999999">
										<td><font color="#800000" size="+1" face="Times New Roman"><%=strAlpha%></font></td>
										</tr><tr><td width='20%' height='20' VALIGN=TOP> 
										
									<%	
									'MySQL = "SELECT specimen.ACCESSION,spdetail.TAXA FROM specimen, spdetail WHERE ((spdetail.taxcd = specimen.taxcd) AND (specimen.TYPE <> ' ') AND (spdetail.TAXA like '"&chr(intIndex)&"%')) ORDER BY specimen.Accession"
									MySQL = "SELECT specimen.ACCESSION, spdetail.Taxa FROM specimen INNER JOIN spdetail ON specimen.TAXCD = spdetail.Taxcd WHERE (spdetail.syncd = '.' AND specimen.TYPE <> ' ' AND specimen.scan='1') AND (spdetail.Taxa LIKE '"&chr(intIndex)&"%') ORDER BY spdetail.TAXA, specimen.ACCESSION" 
									
									Set RS = MyConn.Execute(MySQL)
									while not RS.EOF 
									response.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='../specimen/scripts/specimen.asp?Accession="&RS("ACCESSION")&"' target=_blank>")
									response.write(RS("TAXA"))
									response.write("</a> - <font size=-1 color='#666666'>" & RS("ACCESSION") & "</font><br>")
									RS.movenext
									wend
									%></td></tr>					
									<tr>
									<% if strAlpha <>"Q" then
									response.write("&nbsp; &nbsp; &nbsp;<a href='#top'> <font color='red'> TOP </font></a>")
									end if
									%></tr>
											</table>
									<br>
									<% next 
									case 4
								    response.write("<table><tr><td><a href=type_index.asp> A-C </a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;</td><td><a href=type_index.asp?page=1> D-I </a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;</td><td><a href=type_index.asp?page=2>J-P</a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;</td><td><a href=type_index.asp?page=3> Q-V </a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;</td><td> W-Z &nbsp;</td></tr></table>")
									response.write("&nbsp;&nbsp;&nbsp;")
									For intIndex = 87 to 90
									strAlpha=chr(intIndex) %>
									<a href="#<%=strAlpha%>"> 
									<%=strAlpha%> </a>&nbsp; 
									<% next %>
									<%
									For intIndex = 87 to 90
									strAlpha = chr(intIndex)
 									i=0 %>
										<a NAME="<%=strAlpha%>"></a>
										
										<table width="80%" border="1" cellspacing="2" cellpadding="2" frame="border">
										<tr bgcolor="#999999">
										<td><font color="#800000" size="+1" face="Times New Roman"><%=strAlpha%></font></td>
										</tr><tr><td width='20%' height='20' VALIGN=TOP> 
										
									<%	
									'MySQL = "SELECT specimen.ACCESSION,spdetail.TAXA FROM specimen, spdetail WHERE ((spdetail.taxcd = specimen.taxcd) AND (specimen.TYPE <> ' ') AND (spdetail.TAXA like '"&chr(intIndex)&"%')) ORDER BY specimen.Accession"
									MySQL = "SELECT specimen.ACCESSION, spdetail.Taxa FROM specimen INNER JOIN spdetail ON specimen.TAXCD = spdetail.Taxcd WHERE (spdetail.syncd = '.' AND specimen.TYPE <> ' ' AND specimen.scan='1') AND (spdetail.Taxa LIKE '"&chr(intIndex)&"%') ORDER BY spdetail.TAXA, specimen.ACCESSION" 
									
									Set RS = MyConn.Execute(MySQL)
									while not RS.EOF 
									response.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='../specimen/scripts/specimen.asp?Accession="&RS("ACCESSION")&"' target=_blank>")
									response.write(RS("TAXA"))
									response.write("</a> - <font size=-1 color='#666666'>" & RS("ACCESSION") & "</font><br>")
									RS.movenext
									wend
									%></td></tr>					
									<tr>
									<% if strAlpha <>"W" then
									response.write("&nbsp; &nbsp; &nbsp;<a href='#top'> <font color='red'> TOP </font></a>")
									end if
									%></tr>
											</table>
									<br>
									<% next 
									case else
									response.write("A-C &nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;<a href=type_index.asp?page=1> D-I </a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;<a href=type_index.asp?page=2>J-P</a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;<a href=type_index.asp?page=3> Q-V </a>&nbsp;&nbsp;<font color='red'> | </font>&nbsp;&nbsp;<a href=type_index.asp?page=4> W-Z </a>&nbsp;<br>")
									For intIndex = 65 to 67
									strAlpha=chr(intIndex) %>
									<a href="#<%=strAlpha%>"> 
									<%=strAlpha%> </a>&nbsp; 
									<% next %>
									<%
									For intIndex = 65 to 67
									strAlpha = chr(intIndex)
 									i=0 %>
										<a NAME="<%=strAlpha%>"></a>
										
										<table width="80%" border="1" cellspacing="2" cellpadding="2" frame="border">
										<tr bgcolor="#999999">
										<td><font color="#800000" size="+1" face="Times New Roman"><%=strAlpha%></font></td>
										</tr><tr><td width='20%' height='20' VALIGN=TOP> 
										
									<%	
									'MySQL = "SELECT specimen.ACCESSION,spdetail.TAXA FROM specimen, spdetail WHERE ((spdetail.taxcd = specimen.taxcd) AND (specimen.TYPE <> ' ') AND (spdetail.TAXA like '"&chr(intIndex)&"%')) ORDER BY specimen.Accession"
									MySQL = "SELECT specimen.ACCESSION, spdetail.Taxa FROM specimen INNER JOIN spdetail ON specimen.TAXCD = spdetail.Taxcd WHERE (spdetail.syncd = '.' AND specimen.TYPE <> ' ' AND specimen.scan='1') AND (spdetail.Taxa LIKE '"&chr(intIndex)&"%') ORDER BY spdetail.TAXA, specimen.ACCESSION" 
									
									Set RS = MyConn.Execute(MySQL)
									while not RS.EOF 
									response.write("&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='../specimen/scripts/specimen.asp?Accession="&RS("ACCESSION")&"' target=_blank>")
									response.write(RS("TAXA"))
									response.write("</a> - <font size=-1 color='#666666'>" & RS("ACCESSION") & "</font><br>")
									RS.movenext
									wend
									%></td></tr>					
									<tr>
									<% if strAlpha <>"A" then
									response.write("&nbsp; &nbsp; &nbsp;<a href='#top'> <font color='red'> TOP </font></a>")
									end if
									%></tr>
											</table>
									<br>
									<% next 
									end select
			response.write "</div>"
									%>
									<!--#include virtual="/wisflora/specimen/includes/spec_pub_menu.asp" -->
<br>
<!--#include virtual="/wisflora/specimen/includes/spec_pub_foot.asp" -->

<% '<!--#include virtual="/wisflora/includes/specfooter.asp" --> %>

<!--#include virtual="/wisflora/scripts/dbdisconnect.asp"-->

</body>
</html>
