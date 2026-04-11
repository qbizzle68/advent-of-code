CFLAGS = -O3 -Wno-deprecated-declarations
LIBS = -lcrypto

all: part1 part2

part1: part1.o
	gcc $(CFLAGS) part1.o -o part1 $(LIBS)

part2: part2.o
	gcc $(CFLAGS) part2.o -o part2 $(LIBS)

%.o: %.c
	gcc $(CFLAGS) -c $< -o $@

.PHONY: clean

clean:
	rm -f *.o part1 part2
