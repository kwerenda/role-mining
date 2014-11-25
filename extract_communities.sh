#!/bin/sh
## Usage: ./extract_communities.sh file_with_edges1 file_with_edges2 ...

for arg in "$@"; do
	communities_dir=`ls $arg | cut -d / -f -2`/communities/
	output_file=$communities_dir`ls $arg | cut -d / -f 4- | cut -d \. -f 1`

	echo "Output file: "$output_file | tee -a CFinder.log
	
	./CFinder-2.0.6--1448/CFinder_commandline64 -D \
	-i $1 -l CFinder-2.0.6--1448/licence.txt -o $output_file >> CFinder.log
done