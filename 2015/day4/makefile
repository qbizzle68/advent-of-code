CFLAGS = -O3 -Wno-deprecated-declarations
LIBS = -lcrypto -lm

SRCS = fastmine.c
OBJS = $(SRCS:.c=.o)

TARGET = fastmine
all: $(TARGET)

$(TARGET): $(OBJS)
	gcc $(CFLAGS) $(OBJS) -o $(TARGET) $(LIBS)

%.0: %.c
	gcc $(CFLAGS) -c $< -o $@

.PHONY: clean
clean:
	rm -f $(OBJS) $(TARGET)
