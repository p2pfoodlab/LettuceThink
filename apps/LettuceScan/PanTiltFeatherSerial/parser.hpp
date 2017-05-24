enum _pstate {
  OPCODE = 0,
  SIGN_OR_DIGIT = 1,
  DIGIT = 2,
  COMMAND = 3
};

class Parser 
{
  public:
    int state;
    int opcode;
    int sign;
    int value;
    int absvalue;

  Parser();
  int handle(char c);
};


