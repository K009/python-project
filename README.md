# Algorytm Dijkstry z wykorzystaniem biblioteki pygame

## Jak włączyć projekt

1. Pobierz repozytorium lub sklonuj je
2. Skompiluj plik dijkstra.py poprzez wpisanie w terminal komendy: python dijkstra.py

## Opis projektu

Celem mojego projektu było zaimplementowanie algorytmu Dijkstry w pythonie. Dodatkowo zdecydowałem się użyć biblioteki pygame, w celu przystępnej dla oka wizualizacji działania algorytmu. 

Graf przypomina planszę gry, która składa się z siatki. Siatka składa się z kwadratów, gdzie każdy kwadrat to pojedyńczy wierzchołek, a koszt przejścia z jednego wierzchołka do drugiego jest zależny od koloru kwadratu. Czyli przejście pomiędzy zielonymi kwadratami może mieć koszt równy 2, natomiast przejście między kwadratem zielonym a niebieskim jest niemożliwe, stąd wyrysowana ściezka nigdy nie przechodzi przez niebieskie kwadraty/wierzchołki. 

W programie wykorzystuję szereg funkcji odpowiedzialnych za rysowanie planszy, z pomocą biblioteki pygame. Dodatkowo zaimplementowałem takie funkcje jak draw_grid odpowiedzialną za rysowanie planszy oraz draw_icons, która rysuje wierzchołek początkowy (smoka) oraz wierzchołek końcowy (zamek). 

Sednem programu jest jednak algorytm dijkstry, który zaimplementowałem z wykorzystaniem kolejki priorytetowej. Na początku tworzę tablice, w których będę przechowywał koszty dojścia do poszczególnych wierzchołków w grafie oraz docelową drogę do naszego celu. Do kolejki dodaję najpierw położenia punktu startowego, a następnie dopóki kolejka nie jest pusta usuwam z kolejki kolejne wierzchołki o najniższych priorytetach oraz dla każdego sąsiada bieżącego wierzchołka sprawdzam czy poprzez przejście do danego sąsiada nie dotrzemy do celu szybciej, niż dotychczasowo obraną ścieżką. Na końcu tablica path zwraca najkrótszą ścieżkę do wierzchołka docelowego.
