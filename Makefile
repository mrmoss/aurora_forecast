PROG=bin/forecast_retriever
UNIT=bin/unit_tests
COMMON=
INCLUDE=-Isrc/
OPTS=-O3 -Wall -Wno-unused-but-set-variable -std=c++11

all: $(UNIT) $(PROG)

$(PROG): src/forecast_retriever/main.cpp $(COMMON)
	g++ $(INCLUDE) $(OPTS) $(COMMON) $< -o $@

$(UNIT): src/unit_tests.cpp $(COMMON)
	g++ $(INCLUDE) $(OPTS) $(COMMON) $< -o $@

clean:
	- rm -f $(PROG) $(UNIT)