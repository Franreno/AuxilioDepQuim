COMP = g++
SRC = ./src
INC = -I ./headers
FLAGS = -I/usr/include/postgresql -lpq -std=c++17
OUT = prog

OBJECTS = database_handler.o

all: $(OBJECTS)
	$(COMP) $(SRC)/main.cpp $(OBJECTS) -o $(OUT) $(INC) $(FLAGS)

%.o: $(SRC)/%.cpp
	$(COMP) -c $< $(INC) $(FLAGS) -o $@

run:
	./$(OUT)

clean:
	rm -f *.o *.bin *.zip
	rm prog

zip:
	zip -r zipped.zip Makefile ./src ./headers