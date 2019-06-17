#include <iostream>
#include "tagmapper.h"


u_int TagMapper::druhMap(char c) {
    switch (c) {
      case '-': return 0;
      case 'N': return 1;
      case 'A': return 2;
      case 'P': return 3;
      case 'C': return 4;
      default: return 0;
    }
  }

u_int TagMapper::rodMap(char c) {
    switch (c) {
      case '-': return 5;
      case 'F': return 6;
      case 'I': return 7;
      case 'M': return 8;
      case 'N': return 9;
      default: return 5;
    }
  }

u_int TagMapper::cisloMap(char c) {
    switch (c) {
      case '-': return 10;
      case 'D': return 11;
      case 'P': return 12;
      case 'S': return 13;
      default: return 10;
    }
  }

u_int TagMapper::padMap(char c) {
    if (c == '-' || c == 'X') {
      return 14;
    } else {
      return 14 + (c - '0');
    }
}


u_int TagMapper::verbCisloMap(char c) {
  switch (c) {
    case '-': return 0;
    case 'S': return 1;
    case 'P': return 2;
    default: return 0;
  }
}

u_int TagMapper::verbOsobaMap(char c) {
  switch (c) {
    case '-': return 3;
    case '1': return 4;
    case '2': return 5;
    case '3': return 6;
    default: return 3;
  }
}



