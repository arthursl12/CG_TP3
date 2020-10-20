CC := g++
MYDIR := $(dir $(realpath $(firstword $(MAKEFILE_LIST))))
SRCDIR := src
BIN :=
BUILDDIR := build
TARGET := main

SRCEXT := cpp
CFLAGS := -O3 -std=c++14
LIBS :=
INC := -I include -I third-party -L. 


MODULES = vec3 ray color hittable sphere hittable_list
SOURCES = $(addsuffix .cpp,$(MODULES))
OBJECTS = $(patsubst %.cpp, %.o, $(SOURCES))
TESTS = $(addprefix test_,$(SOURCES))
TESTSEXE = $(addsuffix .exe,$(TESTS))
TESTSEXEDIR = $(addprefix bin/,$(TESTSEXE))
COVER = $(addsuffix .gcov,$(SOURCES))

SOURCEDIR = $(addprefix src/,$(SOURCES))
OBJDIR = $(addprefix build/,$(OBJECTS))
TSTDIR = $(addprefix tests/test_,$(SOURCES))
TGTDIR = $(TARGET)

all: $(TGTDIR)

$(OBJDIR): build/%.o : src/%.cpp
	@echo ""
	@echo OBJETO: $@
	$(shell mkdir -p build)
	$(CC) $(INC) $(CFLAGS) -c $(patsubst build/%.o,src/%.cpp,$@) -o $@

$(TGTDIR): $(OBJDIR)
	@echo ""
	@echo COMPILANDO MAIN
	$(CC) $(INC) $(CFLAGS) $(OBJDIR) $(TARGET).cpp $(LIBS) -o $(TGTDIR)
	@./$(TGTDIR)


comp: $(TGTDIR)
	$(CC) $(INC) $(CFLAGS) $(OBJDIR) $(TARGET).cpp $(LIBS) -o $(TGTDIR)
	# @./main

run:
	@./main

clean:
	$(RM) -r build/* coverage/* *.gcda *.gcno *.gcov *.exe *.o bin/*

.PHONY: clean