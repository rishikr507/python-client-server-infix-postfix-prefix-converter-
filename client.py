import socket

HEADER = 2048
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

PORT = 8000
SERVER = "172.20.10.3"  # The IP address of the server
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Functions to validate different expressions (already provided in your code)
def is_valid_infix(expression):
    operators = set('+-*/')
    parentheses_count = 0
    last_char = ''
    
    for char in expression.split(' '):
        if char.isalnum():  # Operand
            last_char = char
        elif char in operators:  # Operator
            if last_char in operators or last_char == '':
                return False
            last_char = char
        elif char == '(':  # Opening parenthesis
            parentheses_count += 1
            last_char = char
        elif char == ')':  # Closing parenthesis
            parentheses_count -= 1
            if parentheses_count < 0 or last_char in operators:
                return False
            last_char = char
        else:
            return False
    
    return parentheses_count == 0 and last_char not in operators and last_char != '('


def is_valid_postfix(expression):
    tokens = expression.split(' ')
    stack = []
    
    for token in tokens:
        if token.isalnum():  # Operand
            stack.append(token)
        elif token in '+-*/':  # Operator
            if len(stack) < 2:
                return False
            operand2 = stack.pop()
            operand1 = stack.pop()
            stack.append('result')  # Placeholder for result
        else:
            return False
    
    return len(stack) == 1


def is_valid_prefix(expression):
    tokens = expression.split(' ')
    stack = []
    
    for token in reversed(tokens):
        if token.isalnum():  # Operand
            stack.append(token)
        elif token in '+-*/':  # Operator
            if len(stack) < 2:
                return False
            operand1 = stack.pop()
            operand2 = stack.pop()
            stack.append('result')  # Placeholder for result
        else:
            return False
    
    return len(stack) == 1


# Function to send messages and options to the server
def send(msg, op):
    # Send the operation code (option)
    option = op.encode(FORMAT)
    op_length = len(option)
    send_oplen = str(op_length).encode(FORMAT)
    send_oplen += b' ' * (HEADER - len(send_oplen))  # Padding for consistent length
    client.send(send_oplen)  # Send the length of the option
    client.send(option)  # Send the actual option

    # Send the message (expression)
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))  # Padding for consistent length
    client.send(send_length)  # Send the length of the message
    client.send(message)  # Send the actual message

    # Receive the output from the server
    output_length = int(client.recv(HEADER).decode(FORMAT))  # Receive the output length
    output = client.recv(output_length).decode(FORMAT)  # Receive the actual output
    print(output)


# Main loop for user input
ch = True
while ch:
    print("\n1: Prefix to Postfix conversion\n2: Postfix to Prefix conversion")
    print("3: Prefix to Infix conversion\n4: Infix to Prefix conversion")
    print("5: Postfix to Infix conversion\n6: Infix to Postfix conversion")
    print("7: Exit")

    choice = int(input("\nEnter your choice: "))

    if choice == 1:  # Prefix to Postfix conversion
        msg = input("\nEnter prefix expression: ")
        if not is_valid_prefix(msg):
            print("\nInvalid Prefix Expression! Please try again.")
            continue
        send(msg, str(choice))

    elif choice == 2:  # Postfix to Prefix conversion
        msg = input("\nEnter postfix expression: ")
        if not is_valid_postfix(msg):
            print("\nInvalid Postfix Expression! Please try again.")
            continue
        send(msg, str(choice))

    elif choice == 3:  # Prefix to Infix conversion
        msg = input("\nEnter prefix expression: ")
        if not is_valid_prefix(msg):
            print("\nInvalid Prefix Expression! Please try again.")
            continue
        send(msg, str(choice))

    elif choice == 4:  # Infix to Prefix conversion
        msg = input("\nEnter infix expression: ")
        if not is_valid_infix(msg):
            print("\nInvalid Infix Expression! Please try again.")
            continue
        send(msg, str(choice))

    elif choice == 5:  # Postfix to Infix conversion
        msg = input("\nEnter postfix expression: ")
        if not is_valid_postfix(msg):
            print("\nInvalid Postfix Expression! Please try again.")
            continue
        send(msg, str(choice))

    elif choice == 6:  # Infix to Postfix conversion
        msg = input("\nEnter infix expression: ")
        if not is_valid_infix(msg):
            print("\nInvalid Infix Expression! Please try again.")
            continue
        send(msg, str(choice))

    elif choice == 7:  # Exit
        ch = False
        send(DISCONNECT_MESSAGE, str(choice))  # Send disconnect message
        break

    else:
        print("\nWrong choice entered. Please try again.")
