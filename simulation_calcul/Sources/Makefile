compilateur = gcc
debugger = gdb

CFLAGS = -g -Wall -c -Og
LFLAGS = -Wall -o

all: compil clear
	./resultat

pdf: compil clear
	./resultat -PDF

debug: compil clear
	$(debugger) ./resultat

openPM: compil_openMP clear
	./resultat

openPM_pdf: compil_openMP clear
	./resultat -PDF

memcheck: compil_debug clear
	valgrind --tool=memcheck --leak-check=yes --show-reachable=yes --num-callers=20 --track-fds=yes ./resultat

callgrind: compil_debug clear
	valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes --collect-jumps=yes ./resultat
	kcachegrind &

memcheck_pdf: compil_debug clear
	valgrind --tool=memcheck --leak-check=yes --show-reachable=yes --num-callers=20 --track-fds=yes ./resultat -PDF

callgrind_pdf: compil_debug clear
	valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes --collect-jumps=yes ./resultat -PDF
	kcachegrind &


compil: TableauDynamique.o hyper_expo.o simulation.o File.o main.o
	gcc -Wall TableauDynamique.c hyper_expo.c simulation.c File.c main.c -o resultat

compil_debug: TableauDynamique.o hyper_expo.o simulation.o File.o main.o
	gcc -Wall TableauDynamique.c hyper_expo.c simulation.c File.c main.c -o resultat -g

compil_openMP: TableauDynamique.o hyper_expo.o simulation.o File.o main.o
	gcc -Wall -fopenmp TableauDynamique.c hyper_expo.c simulation.c File.c main.c -o resultat

hyper_expo.o: hyper_expo.c
	$(compilateur) $(CFLAGS) hyper_expo.c

simulation.o: simulation.c
	$(compilateur) $(CFLAGS) simulation.c

File.o: File.c
	$(compilateur) $(CFLAGS) File.c

TableauDynamique.o: TableauDynamique.c
	$(compilateur) $(CFLAGS) TableauDynamique.c

main.o: main.c
	$(compilateur) $(CFLAGS) main.c


clear:
	rm -f *.o

clear_all : resultat
	rm resultat
	rm -f *.o
	rm callgrind.out.*
