PROG=bin/forecast_retriever
UNIT=bin/unit_tests
COMMON=src/get_request.cpp src/msl/socket.cpp src/msl/socket_util.cpp src/msl/time_util.cpp
INCLUDE=-Isrc/
OPTS=-O3 -Wall -Wno-unused-but-set-variable -std=c++11

all: $(UNIT) $(PROG)

$(PROG): src/forecast_retriever/main.cpp $(COMMON)
	g++ $(INCLUDE) $(OPTS) $(COMMON) $< -o $@

$(UNIT): src/unit_tests.cpp $(COMMON)
	g++ $(INCLUDE) $(OPTS) $(COMMON) $< -o $@

clean:
	- rm -f $(PROG) $(UNIT)