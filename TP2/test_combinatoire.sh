#!/bin/bash

eval "./extractor.sh $1"

# on appelle le fichier python
echo "cover table generation and checking (this may take some time)"
python3 question1.py $1 arg.txt contraintes.txt commands.txt
echo -e "\e[1;92m 0K \e[0m"
echo -e "\e[1;4mStarting tests on $1\n\e[0m"
while read command; do
    `${command}`
done < commands.txt
echo -e "\e[1;92m 0K \e[0m"
rm arg.txt contraintes.txt commands.txt
