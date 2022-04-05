for dir in $(ls ../data/crawled/poetry/) ; do
	echo $dir ; 
	cat * | grep -i $dir ; 
#	echo "\n\n\n" ; 
done
