import http.server
import socketserver
import json
import ctypes
import os

# Load the C++ shared library (ctypes is built-in, no installation needed)
lib_ext = '.dll' if os.name == 'nt' else '.so'
try:
    cpp_logic = ctypes.CDLL(os.path.abspath(f"logic{lib_ext}"))
except OSError:
    print(f"Warning: Could not find compiled C++ library logic{lib_ext}.")
    cpp_logic = None

class LogicGateHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Serve the HTML file when visiting the root URL
        if self.path == '/':
            self.path = '/index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        # Handle the calculation request from the HTML frontend
        if self.path == '/calculate':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            gate = data.get('gate')
            a = int(data.get('a', 0))
            b = int(data.get('b', 0))
            result = 0

            # Calculation with C++ library if available, otherwise Python
            backend_used = "C++ Library (logic" + lib_ext + ")" if cpp_logic else "Python Fallback Engine"
            expression = ""
            explanation = ""

            gate_upper = (gate or "AND").upper()
            if cpp_logic:
                if gate_upper == "AND": result = cpp_logic.logic_and(a, b)
                elif gate_upper == "OR": result = cpp_logic.logic_or(a, b)
                elif gate_upper == "XOR": result = cpp_logic.logic_xor(a, b)
                elif gate_upper == "NOT": result = cpp_logic.logic_not(a)
                elif gate_upper == "NAND":
                    result = cpp_logic.logic_nand(a, b) if hasattr(cpp_logic, 'logic_nand') else int(not (a & b))
                elif gate_upper == "NOR":
                    result = cpp_logic.logic_nor(a, b) if hasattr(cpp_logic, 'logic_nor') else int(not (a | b))
                elif gate_upper == "XNOR":
                    result = cpp_logic.logic_xnor(a, b) if hasattr(cpp_logic, 'logic_xnor') else int(not (a ^ b))
                else:
                    result = 0
            else:
                if gate_upper == "AND": result = a & b
                elif gate_upper == "OR": result = a | b
                elif gate_upper == "XOR": result = a ^ b
                elif gate_upper == "NOT": result = int(not a)
                elif gate_upper == "NAND": result = int(not (a & b))
                elif gate_upper == "NOR": result = int(not (a | b))
                elif gate_upper == "XNOR": result = int(not (a ^ b))
                else: result = 0

            # Generate descriptive expression and explanation
            if gate_upper == "NOT":
                expression = f"¬({a}) = {result}"
                explanation = f"Inverts the single input: NOT {a} yields {result}"
            elif gate_upper == "AND":
                expression = f"{a} · {b} = {result}"
                explanation = f"Outputs 1 only when both inputs are 1: {a} AND {b} = {result}"
            elif gate_upper == "OR":
                expression = f"{a} + {b} = {result}"
                explanation = f"Outputs 1 if at least one input is 1: {a} OR {b} = {result}"
            elif gate_upper == "XOR":
                expression = f"{a} ⊕ {b} = {result}"
                explanation = f"Outputs 1 when inputs are different: {a} XOR {b} = {result}"
            elif gate_upper == "NAND":
                expression = f"¬({a} · {b}) = {result}"
                explanation = f"Inverted AND: Outputs 0 only when both inputs are 1: NOT({a} AND {b}) = {result}"
            elif gate_upper == "NOR":
                expression = f"¬({a} + {b}) = {result}"
                explanation = f"Inverted OR: Outputs 1 only when both inputs are 0: NOT({a} OR {b}) = {result}"
            elif gate_upper == "XNOR":
                expression = f"¬({a} ⊕ {b}) = {result}"
                explanation = f"Outputs 1 when inputs are identical: NOT({a} XOR {b}) = {result}"

            # Send response back to HTML
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = json.dumps({
                "result": int(result),
                "gate": gate_upper,
                "a": a,
                "b": b,
                "expression": expression,
                "explanation": explanation,
                "backend": backend_used
            })
            self.wfile.write(response.encode('utf-8'))

    def end_headers(self):
        # Enable caching-free response during development
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

# Start the built-in server
PORT = 8000
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), LogicGateHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    httpd.serve_forever()