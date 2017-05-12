compilateur = gcc

CFLAGS = -O2 -g -Wall -c
LFLAGS = -Wall -o

all: compil run


compil: hyper_expo.o simulation.o File.o main.o
	$(compilateur) $(LFLAGS) resultat hyper_expo.o simulation.o File.o main.o
	#$(compilateur) hyper_expo.c simulation.c File.c main.c -o resultat


run:
	./resultat

run_memcheck:
	valgrind --tool=memcheck --leak-check=yes --show-reachable=yes --num-callers=20 --track-fds=yes ./resultat

run_callgrind:
	valgrind --tool=callgrind --dump-instr=yes --simulate-cache=yes --collect-jumps=yes ./resultat
	kcachegrind &

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

memcheck: compil run_memcheck

callgrind: compil run_callgrind
