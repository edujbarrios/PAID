"""
Simple Error Example - Testing AI Debugger
Author: Eduardo J. Barrios (github.com/edujbarrios)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from paid.core.enhanced_debugger import AIDebugger

# Initialize debugger
api_key = input("Enter your API key (or press Enter to use 'Unused'): ").strip()
if not api_key:
    api_key = "Unused"

debugger = AIDebugger(api_key=api_key, use_templates=True)

# Simple buggy code
buggy_code = """
def calculate_average(numbers):
    total = sum(numbers)
    count = len(numbers)
    return total / count

result = calculate_average([])
print(f"Average: {result}")
"""

# Analyze the error
debugger.debug_code(buggy_code)

