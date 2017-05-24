enum _pstate {
  OPCODE = 0,
  SIGN_OR_DIGIT = 1,
  DIGIT = 2,
  COMMAND = 3
};

class Parser 
{
  public:
    char state;
    char opcode;
    int sign;
    int value;
    int absvalue;

  Parser();
  int handle(char c);
};


