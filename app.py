import streamlit as st
import math, operator, re

# -------------------------------
# Calculator Engine (Data Structures)
# -------------------------------
ops = {'+':1, '-':1, '*':2, '/':2, '^':3}
assoc = {'+':'left','-':'left','*':'left','/':'left','^':'right'}
op_funcs = {'+':operator.add,'-':operator.sub,'*':operator.mul,'/':operator.truediv,'^':operator.pow}

def tokenize(expr):
    tokens = re.findall(r'\\d+\\.?\\d*|[+\\-*/^()]|sqrt', expr)
    return tokens

def shunting_yard(tokens):
    output, stack = [], []
    for token in tokens:
        if re.fullmatch(r'\\d+\\.?\\d*', token):
            output.append(token)
        elif token in ops:
            while stack and stack[-1] in ops:
                if (assoc[token] == 'left' and ops[token] <= ops[stack[-1]]) or \
                   (assoc[token] == 'right' and ops[token] < ops[stack[-1]]):
                    output.append(stack.pop())
                else:
                    break
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        elif token == 'sqrt':
            stack.append(token)
    while stack:
        output.append(stack.pop())
    return output

def eval_rpn(rpn):
    stack = []
    for token in rpn:
        if re.fullmatch(r'\\d+\\.?\\d*', token):
            stack.append(float(token))
        elif token in op_funcs:
            b, a = stack.pop(), stack.pop()
            stack.append(op_funcs[token](a,b))
        elif token == 'sqrt':
            a = stack.pop()
            stack.append(math.sqrt(a))
    return stack[0]

def safe_eval(expr):
    if not expr:
        return ""
    return eval_rpn(shunting_yard(tokenize(expr)))

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="🎨 Colourful Calculator", page_icon="🧮", layout="centered")
st.title("🎨 Colourful Calculator")
st.caption("Built with Python, Data Structures (Shunting Yard + RPN), and Streamlit")

# Session state to hold expression
if "expr" not in st.session_state:
    st.session_state.expr = ""

# Display
st.markdown(
    f"""
    <div style="background:#111; color:#fff; padding:12px; border-radius:8px; font-size:28px; text-align:right;">
        {st.session_state.expr or '0'}
    </div>
    """,
    unsafe_allow_html=True
)

# Button grid
buttons = [
    ["C","DEL","(",")","^"],
    ["7","8","9","/","sqrt"],
    ["4","5","6","*",""],
    ["1","2","3","-",""],
    ["0",".","=","+",""]
]

# Colors
colors = {
    "digits": "#2b6fb3",
    "ops": "#ff8c42",
    "eq": "#2bb67d",
    "ctrl": "#d9534f",
    "func": "#7b5cff"
}

# Button handler
def handle_click(label):
    if label == "=":
        try:
            result = safe_eval(st.session_state.expr)
            st.session_state.expr = str(result)
        except Exception as e:
            st.error(f"Error: {e}")
    elif label == "C":
        st.session_state.expr = ""
    elif label == "DEL":
        st.session_state.expr = st.session_state.expr[:-1]
    elif label:
        if label == "sqrt":
            st.session_state.expr += "sqrt("
        else:
            st.session_state.expr += label

# Render buttons
for row in buttons:
    cols = st.columns(len(row))
    for i, label in enumerate(row):
        if not label:
            continue
        if label.isdigit() or label == ".":
            color = colors["digits"]
        elif label in ["+","-","*","/","^"]:
            color = colors["ops"]
        elif label == "=":
            color = colors["eq"]
        elif label in ["C","DEL"]:
            color = colors["ctrl"]
        else:
            color = colors["func"]

        with cols[i]:
            if st.button(label, use_container_width=True):
                handle_click(label)
