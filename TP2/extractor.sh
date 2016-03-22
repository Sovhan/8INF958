#!/bin/bash
#netoyage des entrées
if [ $# -ne 1 ]
then
	echo -e "\e[33mone parameter expected, got ${#}"
	echo -e "usage extractor.sh <app_path>\e[0m"
        exit 1 
fi


# on recupere la sortie du -h dans file.txt
echo -e '\nreading application help'
if [ -n ${1:?} ] 
then
	$1 -h | sed -e '/^$/d' > file.txt
	echo -e '\e[1;92m OK \e[0m'

# on recupere tous les arguments (ligne commence par  -)
	echo -e 'arguments extraction'
	sed '/^ *-/!d' file.txt > arg.txt
	echo -e '\e[1;92m OK \e[0m'
# on recupere toutes les contraintes (contiennent un &)
	echo -e 'constraints extraction'
	sed '/&/!d' file.txt > contraintes.txt
	echo -e "\e[1;92m OK \e[0m"

# on efface les &, = dans contraintes.txt et les virgules dans arg.txt
	echo -e 'arguments and constraints files formating'
	sed -i "s/& //g" contraintes.txt
	sed -i "s/\= //g" contraintes.txt
	sed -i "s/^ *-//g" contraintes.txt
	sed -i "s/,//g" arg.txt
	rm file.txt
	echo -e '\e[1;92m OK \e[0m\n'
fi
