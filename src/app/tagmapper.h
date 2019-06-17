#ifndef TAGMAPPER_H_
#define TAGMAPPER_H_


typedef unsigned int u_int;

class TagMapper {
  public:
    static u_int druhMap(char c);
    static u_int rodMap(char c);
    static u_int cisloMap(char c);
    static u_int padMap(char c);
    static u_int verbCisloMap(char c);
    static u_int verbOsobaMap(char c);
};


#endif

