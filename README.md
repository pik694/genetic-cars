# Generic cars
## O projekcie
Jest to projekt semestralny z przedmiotu ALHE realizowanym w semestrze 2018/2019Z. 
Celem projektu jest wykorzystanie algorytmów genetycznych w celu stworzenia jak najlepszego pojazdu dwukołowego.

## Treść zadania
Korzystając z biblioteki box2d zaimplementuj poznany na wykładzie algorytm (np. ewolucyjny/genetyczny) 
by stworzyć najlepszy model pojazdu o dwóch kołach (taki który dojedzie najdalej). 
Przykładowa wizualizacja symulacji: http://boxcar2d.com/. Do implementacji projektu można wykorzystać pakiet pybox2d 
(Python) https://github.com/pybox2d/pybox2d, który wśród swoich przykładów posiada już środowisko samochodowe.

## Pojazd
Pojazd będzie się składał z:
* dwóch kół, niekoniecznie o tych samych rozmiarach, lecz poruszających się z tą samą prędkością kątową;
* trójkątów łączących koła i tworzących pojazd, ustalamy maksymalną ilość trójkątów na 5;

## Trasy
W ramach projektu stworzymy 3 trasy. 

## Funkcja przystosowania
Każdy fenotyp będzie oceniany na podstawie średniego przebytego dystansu na wszystkich trzech trasach. 
Każdy przejazd będzie miał ograniczony czas do założonego limitu, nie większego niż 1 minuta. 

## Algorytm genetyczny
Wykorzystamy gotową bibliotekę implementującą algorytmy genetyczne - `DEAP`.

### Geny

### Selekcja
Wykorzystane typy selekcji:
* ruletkowa;
* turniejowa;
* progowa.


### Krzyżowanie
Wykorzystane typy krzyżowań:
* jednopunktowe;
* równomierne.

### Mutacja
Typy mutacji:
* bitowa;
* gaussowska.


### Skucesja 
Wykorzystamy zastępowanie elitarne.

## Testowanie

Podczas testowania będziemy tworzyli krotki `{algorytm selekcji, typ krzyżowania, typ mutacji}` 
i dla każdej takiej krotki stworzymy po dwie populacje początkowe. 
Każda z krotek dostanie taką samą liczbę iteracji do wykorzystania - wstępnie szacujemy, że każda z krotek dostanie ok. 
1 tygodnia czasu CPU.
Na podstawie zebranych logów dokonamy analizy zachowania algorytmów ewolucyjnych na zadanym problemie.
 

