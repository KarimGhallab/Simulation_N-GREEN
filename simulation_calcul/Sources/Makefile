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

memcheck_openMP: compil_openMP_debug clear
	./resultat

callgrind_openMP: compil_openMP_debug clear
	./resultat

memcheck_openMP_pdf: compil_openMP_debug clear
	./resultat -PDF

callgrind_openMP_pdf: compil_openMP_debug clear
	./resultat -PDF


memcheck: compil_debug clear
	valgrind --tool=memcheck --leak-check=yes --show-reachable=yes --num-callers=20 --track-fds=yes --track-origins=yes ./resultat

callgrind: compil_debug clear
	valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes --collect-jumps=yes ./resultat
	kcachegrind &

memcheck_pdf: compil_debug clear
	valgrind --tool=memcheck --leak-check=yes --show-reachable=yes --num-callers=20 --track-fds=yes --track-origins=yes ./resultat -PDF

callgrind_pdf: compil_debug clear
	valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes --collect-jumps=yes ./resultat -PDF
	kcachegrind &


compil: TableauDynamiqueEntier.o TableauDynamiqueDouble.o hyper_expo.o CoupleNombreValeur.c simulation.o File.o main.o
	gcc -Wall TableauDynamiqueEntier.c TableauDynamiqueDouble.c hyper_expo.c CoupleNombreValeur.c simulation.c File.c main.c -o resultat -lm

compil_debug: TableauDynamiqueEntier.o TableauDynamiqueDouble.o hyper_expo.o CoupleNombreValeur.c simulation.o File.o main.o
	gcc -Wall TableauDynamiqueEntier.c TableauDynamiqueDouble.c hyper_expo.c CoupleNombreValeur.c simulation.c File.c main.c -o resultat -lm -g

compil_openMP: TableauDynamiqueEntier.o TableauDynamiqueDouble.o hyper_expo.o CoupleNombreValeur.c simulation.o File.o main.o
	gcc -Wall -fopenmp TableauDynamiqueEntier.c TableauDynamiqueDouble.c hyper_expo.c CoupleNombreValeur.c simulation.c File.c main.c -o resultat -lm

compil_openMP_debug: TableauDynamiqueEntier.o TableauDynamiqueDouble.o hyper_expo.o CoupleNombreValeur.c simulation.o File.o main.o
	gcc -Wall -fopenmp TableauDynamiqueEntier.c TableauDynamiqueDouble.c hyper_expo.c CoupleNombreValeur.c simulation.c File.c main.c -o resultat -lm -g


hyper_expo.o: hyper_expo.c
	$(compilateur) $(CFLAGS) hyper_expo.c

CoupleNombreValeur.o: CoupleNombreValeur.c
	$(compilateur) $(CFLAGS) CoupleNombreValeur.c

simulation.o: simulation.c
	$(compilateur) $(CFLAGS) simulation.c

File.o: File.c
	$(compilateur) $(CFLAGS) File.c

TableauDynamiqueEntier.o: TableauDynamiqueEntier.c
	$(compilateur) $(CFLAGS) TableauDynamiqueEntier.c

TableauDynamiqueDouble.o: TableauDynamiqueDouble.c
	$(compilateur) $(CFLAGS) TableauDynamiqueDouble.c

main.o: main.c
	$(compilateur) $(CFLAGS) main.c


clear:
	rm -f *.o
	rm -f ../*.o

clear_all : resultat
	rm resultat
	rm -f *.o
	rm -f ../*.o
	rm -f ../Headers/*.gch
	rm callgrind.out.*
