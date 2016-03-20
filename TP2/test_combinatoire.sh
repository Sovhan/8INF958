#!/bin/bash

`./extractor.sh /home/stev/tp2-app.sh`

# on appelle le fichier python
echo "cover table generation (this may take some time)"
python3 question1.py $1 arg.txt contraintes.txt commands.txt

echo "Start testing"
while read command; do
    `$(command)`
done < commands.txt
