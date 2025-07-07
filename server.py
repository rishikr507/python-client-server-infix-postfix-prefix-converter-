import socket
import threading

HEADER = 2048
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

SERVER = socket.gethostbyname(socket.gethostname())  # Use the server's local IP
PORT = 8000
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Helper Functions for Conversions

def precedence(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    return 0

def infix_to_postfix(expression):
    stack = []  # Stack to hold operators
    postfix = []  # List for the output (postfix expression)
    
    for char in expression.split(' '):  # Use split(' ') explicitly
        if char.isalnum():  # Operand
            postfix.append(char)
        elif char == '(':  # Opening parenthesis
            stack.append(char)
        elif char == ')':  # Closing parenthesis
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())  # Pop from stack to output
            stack.pop()  # Pop the '(' from the stack
        else:  # Operator
            while stack and precedence(stack[-1]) >= precedence(char):
                postfix.append(stack.pop())  # Pop from stack to output
            stack.append(char)

    # Pop all remaining operators
    while stack:
        postfix.append(stack.pop())
    
    return ' '.join(postfix)  # Join into string


def infix_to_prefix(expression):
    # Step 1: Reverse the expression
    expression = expression[::-1]
    
    # Step 2: Replace parentheses
    expression = ''.join([')' if char == '(' else '(' if char == ')' else char for char in expression])
    
    # Step 3: Convert to postfix
    postfix = infix_to_postfix(expression)
    
    # Step 4: Reverse the postfix to get prefix
    return postfix[::-1]


def prefix_to_infix(prefix):
    stack = []
    
    for token in reversed(prefix.split(' ')):  # Use split(' ') explicitly
        if token.isalnum():  # Operand
            stack.append(token)
        else:  # Operator
            operand1 = stack.pop()
            operand2 = stack.pop()
            new_expr = f"({operand1} {token} {operand2})"
            stack.append(new_expr)
    
    return stack.pop()


def postfix_to_infix(postfix):
    stack = []
    
    for token in postfix.split(' '):  # Use split(' ') explicitly
        if token.isalnum():  # Operand
            stack.append(token)
        else:  # Operator
            operand2 = stack.pop()
            operand1 = stack.pop()
            new_expr = f"({operand1} {token} {operand2})"
            stack.append(new_expr)
    
    return stack.pop()


def postfix_to_prefix(postfix):
    stack = []
    
    for token in postfix.split(' '):  # Use split(' ') explicitly
        if token.isalnum():  # Operand
            stack.append(token)
        else:  # Operator
            operand2 = stack.pop()
            operand1 = stack.pop()
            new_expr = f"{token} {operand1} {operand2}"
            stack.append(new_expr)
    
    return stack.pop()


def prefix_to_postfix(prefix):
    stack = []
    
    for token in reversed(prefix.split(' ')):  # Use split(' ') explicitly
        if token.isalnum():  # Operand
            stack.append(token)
        else:  # Operator
            operand1 = stack.pop()
            operand2 = stack.pop()
            new_expr = f"{operand1} {operand2} {token}"
            stack.append(new_expr)
    
    return stack.pop()


def handle_client(conn, addr):
    print(f"\n[ NEW CONNECTION ] {addr} is connected.\n")
    connected = True

    while connected:
        # Receive the option length and option
        option_length = int(conn.recv(HEADER).decode(FORMAT))  # Receive the option length
        option = int(conn.recv(option_length).decode(FORMAT))  # Receive the actual option

        # Receive the message length and the message
        msg_length = int(conn.recv(HEADER).decode(FORMAT))  # Receive the message length
        message = str(conn.recv(msg_length).decode(FORMAT))  # Receive the actual message

        if message == DISCONNECT_MESSAGE:
            print(f"\n[ REQUEST ] {addr} sent a request to disconnect\n")
            connected = False
            response= "\ndisconnected from server\n".encode(FORMAT)
            print(f"\n[ DISCONNECT ] {addr} disconnected from server \n")

        elif option == 1:  # Prefix to Postfix
            print(f"\n[ REQUEST ] {addr} sent a prefix expression to get postfix expression\n")
            output = prefix_to_postfix(message)
            response = f"\nthe postfix expression for given prefix string is: {output}\n".encode(FORMAT)

        elif option == 2:  # Postfix to Prefix
            print(f"\n[ REQUEST ] {addr} sent a postfix expression to get prefix expression\n")
            output = postfix_to_prefix(message)
            response = f"\nthe prefix expression for given postfix string is: {output}\n".encode(FORMAT)

        elif option == 3:  # Prefix to Infix
            print(f"\n[ REQUEST ] {addr} sent a prefix expression to get infix expression\n")
            output = prefix_to_infix(message)
            response = f"\nthe infix expression for given prefix string is: {output}\n".encode(FORMAT)

        elif option == 4:  # Infix to Prefix
            print(f"\n[ REQUEST ] {addr} sent an infix expression to get prefix expression\n{message}\n")
            output = infix_to_prefix(message)
            response = f"\nthe prefix expression for given infix string is: {output}\n".encode(FORMAT)

        elif option == 5:  # Postfix to Infix
            print(f"\n[ REQUEST ] {addr} sent a postfix expression to get infix expression\n")
            output = postfix_to_infix(message)
            response = f"\nthe infix expression for given postfix string is: {output}\n".encode(FORMAT)

        elif option == 6:  # Infix to Postfix
            print(f"\n[ REQUEST ] {addr} sent an infix expression to get postfix expression\n{message}\n")
            output = infix_to_postfix(message)
            response = f"\nthe postfix expression for given infix string is: {output}\n".encode(FORMAT)

        # Send the response back to the client
        response_length = len(response)
        send_length = str(response_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))  # Padding for consistent length
        conn.send(send_length)  # Send the length of the response
        conn.send(response)  # Send the actual response


# Start server and listen for connections
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}\n")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


print("[STARTING] Server is starting...")
start()
