#!/bin/sh
## Usage: ./extract_communities.sh file_with_edges1 file_with_edges2 ...

#cfinder=./CFinder-2.0.6--1448/CFinder_commandline64
cfinder=/Applications/CFinder_commandline_mac

for arg in "$@"; do
	communities_dir=`ls $arg | cut -d / -f -2`/communities/
	output_dir=$communities_dir`ls $arg | cut -d / -f 4- | cut -d \. -f 1`

	echo "Output dir: "$output_dir | tee -a CFinder.log
	
#	./CFinder-2.0.6--1448/CFinder_commandline64 -D \
	${cfinder} -D \
	-i $arg -l CFinder-2.0.6--1448/licence.txt -o $output_dir >> CFinder.log
done
