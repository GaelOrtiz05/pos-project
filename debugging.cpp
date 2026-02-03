// This will not actually run in the final program, only exists to test the C++
// Code without needing the gui
#include "POS.hpp"

int main() {
  POS myPOS;
  myPOS.initializeMenu();
  myPOS.display();
  myPOS.clear();
  myPOS.display();
}
