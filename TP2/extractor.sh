/home/stev/tp2-app.sh -h | sed -e '/^$/d' > file.txt
sed '/^ -/!d' file.txt > arg.txt

#grep '[-]' file.txt | awk '$0!~ /^ / {print}'
#grep '^-.*' file.txt > arg.txt
# on efface les lignes vides
#pour chaque line il faut matcher avec commence par -

# lire mot par mot
#for line in $(cat file.txt);
#do
	#echo "$line";
#done
echo "test"
# lire line par line
while read line
do
	#echo "$line"
	#echo "$line" | sed -e '/^-/!d' > arg.txt
	echo "$line" | sed -n '/^-/p'
done < contraintes.txt
