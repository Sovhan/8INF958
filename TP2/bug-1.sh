#!/bin/bash
echo "ceci est le programme pour tester le bug 1"
echo "apres de nombreux tests nous avons reussi a tester sur libre office 3 et 5 via une VM que nous avons cree"
echo "note importante : avant toute chose il faut avoir modifie le parametre de securite des macros :"
echo "- ouvrir libre office"
echo "-dans tools -> options -> security -> macro security -> modifier la securite a medium"
echo "sur le serveur du cours il nous manque des composants afin de tester ce bug de maniere automatique :"
echo "- at-spi"
echo "nous avons aussi reussi a prouver que ce bug, qui normalement a ete corrige, n'a ete que contourne (cf explication en texte dans le document libre office docPourBug1.ods"
 

libreoffice -o docPourBug1.ods &
python question2vb.py &
