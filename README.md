# Praxiswerkstatt Mustererkennung

Sokoban (jpn. "Lagerhausverwalter") ist ein japanisches Computerspiel, indem mit einer Spielfigur Kisten auf Zielfelder bewegt werden müssen. Hierbei kann lediglich eine Kiste in vier Richtungen geschoben werden. Das Bewegen mehrerer Kisten sowie Ziehen oder diagonales bewegen ist nicht möglich. Ziel des Spiels ist es, alle Kisten mit möglichst wenig Schritten auf die vorgesehenen Zielfelder zu bewegen.

Autoren: Jan Hakmann, Philipp Wolters

## Projektideen

- RNN Solver für Sokoban
- GAN Level Generator für Sokoban

Mit Hilfe von Machine Learning sollen auf Basis bekannter und gelöster Level ein Solver erstellt werden. Es soll möglich sein, den Solver auf neue Level anzuwenden.

Nebst der Lösung vorhandener Level, kann das Projekt durch die Generierung von Level erweitert werden. Dabei sollen die generierten Level durch den eigenen Solver gelöst werden können.

## Ablauf

  1. [Datenkorpus](./data/1_original) mit Sokoban Leveln finden
  2. Daten in standardisierte [Form](./data/2_import) bringen
  3. vorhandenen [Solver](./data/3_solved) verwenden um [Trainingsdaten](./data/4_train) zu generieren
  4. Netz trainieren
  5. Neue Level anwenden

## Literatur/Links

- Level: http://www.sourcecode.se/sokoban/levels/
- Solver: http://bach.istc.kobe-u.ac.jp/copris/puzzles/sokoban/
- _Generation of Sokoban Stages using Recurrent Neural Networks_
- _PROCEDURAL GENERATION OF SOKOBAN LEVELS_

## Usage

- Poetry: https://poetry.eustace.io/docs/#installation
