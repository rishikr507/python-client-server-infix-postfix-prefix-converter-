# Socket-Based Expression Converter (Prefix/Infix/Postfix) 📤📥

A Python client-server project to convert between different mathematical expression formats — prefix, infix, and postfix — using socket programming. The project includes client-side validation and structured message handling between client and server using fixed-length headers.

## 💡 Features
- 🔗 Client-Server architecture using Python sockets  
- 🔠 Supports 6 types of expression conversions:  
  - Prefix → Postfix  
  - Postfix → Prefix  
  - Prefix → Infix  
  - Infix → Prefix  
  - Postfix → Infix  
  - Infix → Postfix  
- ✅ Validates expression format before sending to server  
- 📦 Structured data transmission (fixed-size headers)  
- 🔁 Server uses threading to handle multiple clients  

## 🛠️ Technologies Used
- Python 3  
- `socket` module for networking  
- `threading` for concurrent client handling  
- Custom logic for expression parsing/validation  

## 🚀 How to Run the Project  
✅ Make sure Python 3 is installed on your system.

1. Start the Server  
Open a terminal and run:  
python server.py

2. Start the Client  
Open another terminal and run:  
python client.py

3. Choose a Conversion Option  
From the menu:  
1: Prefix to Postfix conversion  
2: Postfix to Prefix conversion  
3: Prefix to Infix conversion  
4: Infix to Prefix conversion  
5: Postfix to Infix conversion  
6: Infix to Postfix conversion  
7: Exit  

Then enter the expression (space-separated), e.g.:  
+ A B  
A B +  
( A + B ) * C  

## ⚠️ Expression Input Rules
- Use space between tokens (e.g., A + B, not A+B)  
- Variables or constants can be any alphanumeric token  
- Supported operators: + - * /  
- Balanced parentheses required in infix  

## 🔐 Communication Protocol
- Fixed HEADER size: 2048 bytes  
- Each message includes operation code and expression  
- Server sends back result with description  

## 📌 Example Conversion  
Input (choice 1): + A B  
Output: the postfix expression for given prefix string is: A B +

## 👨‍💻 About Me
I'm Rishi Kumar, currently pursuing MCA from NIT Patna.  
I'm passionate about Python, AI/ML, and backend systems.  
I build projects that solve real-world problems through clean code and collaboration.

## 📄 License
This project is licensed under the MIT License.
