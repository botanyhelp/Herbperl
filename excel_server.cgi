#!/usr/bin/perl
# inputspecimen_excel_server.cgi 
#this program listens for tcp connections at 127.0.0.1:8888 and 
# when it gets a connection, it runs rsync to copy over the newly-
# created Excel spreadsheets from /var/www/excel/ to /var/www/html/excel
#
#use strict;
#use warnings;
use IO::Socket;
my $server;
my $client;
#always running, rsync is run once per connection, so we need to restart the 
# server every time rsync is run:
while(1 == 1) {
	# establish $server object,bind and listen.
	$server = IO::Socket::INET->new(LocalPort => 8888,
	                                Type      => SOCK_STREAM,
	                                Proto     => 'tcp',
	                                Reuse     => 1,
	                                Listen    => 10 )
	  or die "making socket: $@\n";
	#wait for a client connection,
	while($client = $server->accept()){
                #received connection, and so 'rsync -r /var/www/excel/ /var/www/html/excel/'\n";
                system("/bin/sync") and warn "system() returned a funny exit code\n";
                system("/usr/bin/rsync -r /var/www/excel/ /var/www/html/excel/") and warn "system() returned a funny exit code\n";
	}
	#after running, close the server:
	close($server);
}
