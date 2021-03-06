#!/usr/bin/env perl

#
# Copyright (c) 2008 Robert Blake
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. All advertising materials mentioning features or use of this software
#    must display the following acknowledgement:
#        This product includes software developed by
#        CiteULike <http://www.citeulike.org> and its
#        contributors.
# 4. Neither the name of CiteULike nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY CITEULIKE.ORG AND CONTRIBUTORS
# ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE FOUNDATION OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#

use LWP::Simple;
use strict;
use HTML::Entities;

binmode STDOUT, ":utf8";



my $unclean_url = <>;

chomp($unclean_url);

my $clean_url;
my $doi;

if ($unclean_url =~ m,^https?://csdl\d*\.computer\.org(\.[^/]+)?/persagen/.*DOI=([0-9.a-zA-Z/]+),) {
	$doi = $2;
} elsif ($unclean_url =~ m,^https?://[^/]+\.computer\.org/portal/web/csdl/doi/(\d{2}[.]\d{4}/[^/?&]+),) {
	$doi = $1
} elsif ($unclean_url =~ m{http://[^/]+\.computer.org/portal/web/csdl/abs/}) {
	my $data = get $unclean_url;
	$data =~ m{>http://doi.ieeecomputersociety.org/([^<]*)};
	$doi = $1;
}

if (not $doi) {
  print "status\tnot_interested\n";
  exit;
}

$clean_url = "http://www2.computer.org/plugins/dl/doi/$doi";


my $data = "";
$data = get $clean_url;
if (not $data) {
  print "status\terr\tCouldn't connect to $clean_url\n";
  exit;
}

# Get the bibtex info:

my $bibtex_url = "http://www.computer.org/plugins/dl/citation/abs/bibtex/description/doi/$doi.bib";
my $bibtex = get $bibtex_url;
$bibtex =~ s/\r/\n/g;

print "begin_bibtex\n";
print "$bibtex\n";
print "end_bibtex\n";


print "begin_tsv\n";
print "linkout\tCSDL\t\t$doi\t\t\n";
print "linkout\tDOI\t\t$doi\t\t\n";

# Get the abstract from the page.
if ($data =~ m{<div class="abs-articlesummary">(.*?)</div>}s) {
	my $abstract = $1;
	$abstract =~ s,<[^>]+>,,gs;
	$abstract =~ s/&#822[0123];/"/gs; # microsoft smart double quotes
	$abstract =~ s/&#821[67];/'/gs; # microsoft smart single quotes
	decode_entities($abstract);
	$abstract =~ s/^\s*Abstract\W+//;
	print "abstract\t$abstract\n";
}

print "end_tsv\n";

print "status\tok\n";

exit;

