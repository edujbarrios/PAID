<div align="center">

<img src="assets/paid.png" alt="PAID Logo" width="370" />

# 🐛 PAID: Python AI Debugger

**_"The AI-aware debugger that keeps you AI-free while coding"_**

[![Status](https://img.shields.io/badge/status-on%20development-yellow?style=flat&labelColor=1a1a1a&color=FFD700)](https://github.com/edujbarrios/PAID)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg?style=flat&labelColor=1a1a1a&color=00D9FF)](https://www.python.org/downloads/)
[![Powered by](https://img.shields.io/badge/powered%20by-llm7.io-orange?style=flat&labelColor=1a1a1a&color=FF6B35)](https://llm7.io)

**Future goal:** Transform this into a lightweight desktop app, A small pop-up window you can keep alongside your editor during coding sessions.
**Contributions are welcome!**


</div>

---

##  Quick Start

```bash
# Clone the repository
git clone https://github.com/edujbarrios/PAID.git

# Navigate to the directory
cd PAID

# Install dependencies
pip install -r requirements.txt

# Run simple error example
python paid/examples/simple_error.py
```

---

## 📋 Usage

### Basic Usage Pattern

The debugger analyzes Python code strings that contain errors. Here's the complete pattern:

1. **Code must be a string**: Use triple quotes `"""` for multi-line code
2. **Include complete context**: The code string should be executable and contain the error
3. **API key**: Use `"Unused"` for testing or get your own at [llm7.io](https://token.llm7.io/)
4. **Templates**: Set `use_templates=True` to use Jinja2 templates for better prompts
   - 📂 Check [paid/prompts/](paid/prompts/) to see the Jinja2 template used for error analysis.

### Usage Methods

#### Method 1: Debug a Python File

```python
from paid.core.enhanced_debugger import AIDebugger

debugger = AIDebugger(api_key="Unused")
debugger.debug_file("path/to/your_script.py")
```

#### Method 2: Quick Function Call

```python
from paid.core.debugger import debug_with_ai

buggy_code = """
age = "25"
next_year = age + 1
"""

debug_with_ai(buggy_code, api_key="Unused")
```

#### Method 3: AutoDebug Context Manager

```python
from paid.core.debugger import AutoDebug

with AutoDebug(api_key="Unused"):
    # Any error here will be automatically caught and explained
    x = 10 / 0
```

---

## Example generated AI powered output

```txt
======================================================================
🔍 ERROR DETECTED - Analyzing with AI...
======================================================================

Certainly! Let's break down the error in a clear and structured way:

### 1. WHAT HAPPENED
The error is a `ZeroDivisionError`, which means the code tried to divide a number by zero, and this is not allowed in mathematics (or in Python).

### 2. WHERE IT OCCURS
The error occurs on this line in your `calculate_average` function:
`return total / count`

### 3. WHY IT OCCURS
The root cause of the error is that the `count` variable is zero. The function `calculate_average` attempts to compute the average of a list of numbers by dividing the sum of those numbers by the number of elements in the list. However, when the list is empty (`[]`), the `len(numbers)` returns zero, leading to a division by zero.

### 4. HOW TO FIX IT
To fix this error, you need to add a check to ensure that the list is not empty before performing the division. Here's the corrected code with added checks:

def calculate_average(numbers):
    if len(numbers) == 0:  # Check if the list is empty
        return None  # Return None or any other appropriate value or handle the case as needed
    total = sum(numbers)
    count = len(numbers)
    return total / count

result = calculate_average([])  # This will return None
print(f"Average: {result}")  # Output: Average: None

Alternatively, you could print a message if the list is empty:

def calculate_average(numbers):
    if len(numbers) == 0:
        print("Cannot calculate average of an empty list.")
        return None  # Or handle it in some other way
    total = sum(numbers)
    count = len(numbers)
    return total / count

result = calculate_average([])
print(f"Average: {result}")  # Output: Cannot calculate average of an empty list. Average: None

### 5. BEST PRACTICES
To avoid this kind of error in the future, consider these defensive programming techniques:

- **Input Validation**: Always check if the input list is empty before performing operations that assume non-empty lists.
- **Handling Edge Cases**: Think about what should happen when you receive an empty list or other edge cases.
- **Graceful Degradation**: Ensure your function can handle unexpected inputs gracefully, either by returning a default value, printing an error message, or raising a custom exception.

Here's an example with a custom exception for better handling:

class EmptyListError(Exception):
    pass

def calculate_average(numbers):
    if len(numbers) == 0:
        raise EmptyListError("Cannot calculate average of an empty list.")
    total = sum(numbers)
    count = len(numbers)
    return total / count

try:
    result = calculate_average([])
    print(f"Average: {result}")
except EmptyListError as e:
    print(e)  # Output: Cannot calculate average of an empty list.

This way, you clearly indicate when an empty list is provided, and the function behavior is well-defined for such cases.

By following these practices, you will be better prepared to handle similar issues in your code.
```

---

## 🎯 AI Model Selection

llm7.io supports different model types for different analysis needs:

```python
debugger.debug_code(code, model="fast")    # Quick responses
debugger.debug_code(code, model="default") # Balanced (default)
debugger.debug_code(code, model="pro")     # Deep analysis
```

---

## 💡 Requirements

- Python 3.7+
- `openai` package (required)
- `jinja2` package (optional, for template support)
- Internet connection
- Free API key from [llm7.io](https://token.llm7.io/) or use `"Unused"`

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation


---

## 👨‍💻 Author

**Eduardo J. Barrios**
- GitHub: [@edujbarrios](https://github.com/edujbarrios)
- Powered by [llm7.io](https://llm7.io)

---


