#include "parser.hpp"

Parser::Parser()
{
  state = OPCODE;
  opcode = 0;
  sign = 1;
  value = 0;
  absvalue = 0;
}

int Parser::handle(char c)
{
    if (c >= 'a' && c <= 'z') { 
      if (state == OPCODE || state == COMMAND) {
        opcode = c;
        state = SIGN_OR_DIGIT;
        value = 0;
      } else state = OPCODE;
    } else if (c == '-') {
      if (state == SIGN_OR_DIGIT) {
        sign = -1;
        state = DIGIT;
      } else state = OPCODE; 
    } else if (c >= '0' && c <= '9') {
      if (state == SIGN_OR_DIGIT) {
        sign = 1;
        value = c - '0';
        state = DIGIT;
      } else if (state == DIGIT) {
        value = value * 10 + (c - '0');
      } else state = OPCODE; 
    } else if (c == ';' || c == ' ' || c == '\n' || c == '\r' || c == '\t') {
      if (state == DIGIT) {
        absvalue = value;
        value = sign * value;
        state = COMMAND;
      } else state = OPCODE; 
    } else {
      state = OPCODE;
    }
    return state;
}
