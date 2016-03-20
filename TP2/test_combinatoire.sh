#!/bin/bash

`./extractor.sh $1`

# on appelle le fichier python
echo "cover table generation (this may take some time)"
python3 question1.py $1 arg.txt contraintes.txt commands.txt

echo "Start testing"
while read command; do
    echo "${command}"
    `${command}`
done < commands.txt
