CXX ?= g++
PROGRAM = diakritik
CXXFILES = main.cc data.cc parser.cc indicators.cc hashmap.cc tagmapper.cc
OBJS = $(CXXFILES:.cc=.o)
DEPDIR = .deps
CXXFLAGS = `pkg-config --cflags gtkmm-3.0` -std=c++17 -Wall -g
LIBS = `pkg-config --libs gtkmm-3.0`


all: $(PROGRAM)

-include $(OBJS:%.o=$(DEPDIR)/%.Po)

%.o: %.cc
	@mkdir -p $(DEPDIR)
	$(CXX) -MT $@ -MD -MP -MF $(DEPDIR)/$*.Tpo -c -o $@ $(CXXFLAGS) $<
	@mv -f $(DEPDIR)/$*.Tpo $(DEPDIR)/$*.Po

$(PROGRAM): $(OBJS)
	$(CXX) -o $(PROGRAM) $(OBJS) $(LIBS)

clean:
	rm -f $(OBJS)
	rm -f $(PROGRAM)
	rm -rf $(DEPDIR)

install:
	@mkdir -p ~/.local/share/applications
	sed -e "s#@bindir@#$$PWD#" diakritik.desktop > ~/.local/share/applications/$(PROGRAM).desktop

run:
	./diakritik
