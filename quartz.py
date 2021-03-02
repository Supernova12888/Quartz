# INIT
# Initialize the basic things

from strings_with_arrows import *

DIGITS = '0123456789'



# ERRORS
# Handles all the errors in the user's code

# Parent class of all the types of errors
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details
    
    # Returns the error
    def as_string(self):
        result = f"  {self.error_name}: {self.details}"
        result += f"\n    at {self.pos_start.fn}:{self.pos_start.ln}:{self.pos_start.col}"
        result += "\n    " + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

# Character error
class CharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'CharError', details)

# Syntax error
class SyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=""):
        super().__init__(pos_start, pos_end, 'SyntaxError', details)

# Runtime error
class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end, 'RuntimeError', details)
        self.context = context
    
    # Returns the error
    def as_string(self):
        result = self.generate_traceback()
        result += f"{self.error_name}: {self.details}\n"
        result += "  " + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result
    
    # Generate traceback
    def generate_traceback(self):
        result = ""
        pos = self.pos_start
        ctx = self.context

        # Loop each part of the trace
        while ctx:
            result = f"\n    at {pos.fn}:{str(pos.ln + 1)}:{str(pos.col + 1)} in {ctx.display_name}\n    " + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        
        return "  Traceback (most recent call last):" + result



# POSITION
# Handles the position of the user's code

class Position:
    # Init
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    # Advance
    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0
        
        return self

    # Copy
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)



# TOKENS
# Splits everything in the code into small sections

TT_INT		= 'INT'
TT_FLOAT    = 'FLOAT'
TT_PLUS     = 'PLUS'
TT_MINUS    = 'MINUS'
TT_MULT     = 'MULT' # ?!?!?!
TT_DIV      = 'DIV'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'
TT_EOF		= 'EOF'

class Token:
    # Init
    def __init__(self, typ, value=None, pos_start=None, pos_end=None):
        self.type = typ
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()
        
        if pos_end:
            self.pos_end = pos_end
	
    # Repr
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'



# LEXER

class Lexer:
    # Init
    def __init__(self, fn, text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()
	
    # Advance
    def advance(self):
        self.pos.advance(self.current_char)
        if self.pos.idx < len(self.text):
            self.current_char = self.text[self.pos.idx]
        else:
            self.current_char = None

    # Make tokens
    def make_tokens(self):
        tokens = []

        # Checks if current character is a valid token type
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '+':
                tokens.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(TT_MULT, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN, pos_start=self.pos))
                self.advance()
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], CharError(pos_start, self.pos, "Unexpected '" + char + "'")
        
        # Puts all the tokens together and then return it
        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    # Used for making a number node
    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        # Puts each digit together into a number
        while self.current_char != None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()
        
        # Return different things depending on the dot count in the number
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)



# NODES

class NumberNode:
    # Init
    def __init__(self, tok):
        self.tok = tok
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    
    # Repr
    def __repr__(self):
        return f'{self.tok}'

class BinOpNode:
    # Init
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    # Repr
    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'

class UnaryOpNode:
    # Init
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node
        self.pos_start = self.op_tok.pos_start
        self.pos_end = node.pos_end

    # Repr
    def __repr__(self):
        return f'({self.op_tok}, {self.node})'



# PARSE RESULT
# Handles the result of the parser

class ParseResult:
    # Init
    def __init__(self):
        self.error = None
        self.node = None
    # Register
    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error: self.error = res.error
            return res.node
        return res

    # Success
    def success(self, node):
        self.node = node
        return self

    # Failure
    def failure(self, error):
        self.error = error
        return self



# PARSER
# Divide the user's code into a tree

class Parser:
    # Init
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
    
    # Advance
    def advance(self, ):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    # Parse the user's code
    def parse(self):
        res = self.expr()

        # If there is an syntax error, throw the error
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(SyntaxError(
                self.current_tok.pos_start,
                self.current_tok.pos_end,
                "Expected '+', '-', '*' or '/'"
            ))
        
        # If no syntax error, return result
        return res

    # Handles factors
    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))
        elif tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))
        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(SyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))
        
        # If no number is found, an error is thrown
        return res.failure(SyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int or float"
        ))

    # Term
    def term(self):
        return self.bin_op(self.factor, (TT_MULT, TT_DIV))

    # Expression
    def expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    # Binary operation
    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        
        if res.error:
            return res
        
        # Conbine left factor and right factor with the operator in the middle
        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)
        
        return res.success(left)



# RUNTIME RESULT
# Keeps track of the current result and errors

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None
    
    # Register
    def register(self, res):
        if res.error:
            self.error = res.error
        return res.value
    
    # Success
    def success(self, value):
        self.value = value
        return self
    
    # Failure
    def failure(self, error):
        self.error = error
        return self



# VALUES
# Handles the different types of values in the language

class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()
    
    # Set the position
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    # Set the context
    def set_context(self, context=None):
        self.context = context
        return self
    
    # Add numbers
    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
    
    # Subtract numbers
    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
    
    # Multiply numbers
    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
    
    # Divide numbers
    def dived_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(
                    other.pos_start, other.pos_end,
                    "Cannot divide by zero",
                    self.context
                )
            return Number(self.value / other.value).set_context(self.context), None
    
    def __repr__(self):
        return str(self.value)



# CONTEXT

class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos



# INTERPRETER

class Interpreter:
    # Visit
    def visit(self, node, context):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)
    
    # No visit
    def no_visit_method(self, node, context):
        raise Exception(f"No visit_{type(node).__name__} method defined")
    
    # Visit each node type
    # Number node
    def visit_NumberNode(self, node, context):
        return RTResult().success(
            Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    # Binary operator node
    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res
        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

        # Checks if the operator is valid
        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MULT:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.dived_by(right)
        
        # Checks if there is an error
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))
    
    # Unary operator node
    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.error:
            return res
        
        error = None

        # Checks plus and minus operators
        if node.op_tok.type == TT_MINUS:
            number, error = number.multed_by(Number(-1))
        
        if error:
            return res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start, node.pos_end))



# RUN
# Run the user's code

def run(fn, text):
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error
    
    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error
    
    # Run the actual code
    interpreter = Interpreter()
    context = Context("<program>")
    result = interpreter.visit(ast.node, context)

    return result.value, result.error






