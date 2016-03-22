# on recupere la sortie du -h dans file.txt
#echo "reading application help"
$1 -h | sed -e '/^$/d' > file.txt

# on recupere tous les arguments (ligne commence par  -)
#echo "arguments extraction"
sed '/^ *-/!d' file.txt > arg.txt
# on recupere toutes les contraintes (contiennent un &)
#echo "constraint extraction"
sed '/&/!d' file.txt > contraintes.txt


# on efface les &, = dans contraintes.txt et les virgules dans arg.txt
sed -i "s/& //g" contraintes.txt
sed -i "s/\= //g" contraintes.txt
sed -i "s/^ *-//g" contraintes.txt
sed -i "s/,//g" arg.txt
rm file.txt
