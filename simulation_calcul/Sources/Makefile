compilateur = gcc

CFLAGS = -g -Wall -c -Og
LFLAGS = -Wall -o

all: clear compil
	./resultat

pdf: clear compil
	./resultat PDF

memcheck: clear compil
	valgrind --tool=memcheck --leak-check=yes --show-reachable=yes --num-callers=20 --track-fds=yes ./resultat

callgrind: clear compil
	valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes --collect-jumps=yes ./resultat
	kcachegrind &

memcheck_pdf: clear compil
	valgrind --tool=memcheck --leak-check=yes --show-reachable=yes --num-callers=20 --track-fds=yes ./resultat -PDF

callgrind_pdf: clear compil
	valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes --collect-jumps=yes ./resultat -PDF
	kcachegrind &


compil: hyper_expo.o simulation.o File.o main.o
	#$(compilateur) $(LFLAGS) resultat hyper_expo.o simulation.o File.o main.o
	#clear
	gcc -Wall hyper_expo.c simulation.c File.c main.c -o resultat -g


hyper_expo.o: hyper_expo.c
	$(compilateur) $(CFLAGS) hyper_expo.c

simulation.o: simulation.c
	$(compilateur) $(CFLAGS) simulation.c

File.o: File.c
	$(compilateur) $(CFLAGS) File.c

main.o: main.c
	$(compilateur) $(CFLAGS) main.c


clear:
	rm -f *.o

clear_all : resultat
	rm resultat
	rm -f *.o
	rm callgrind.out.*
