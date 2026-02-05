"""
Test suite for AI Debugger
Author: Eduardo J. Barrios (github.com/edujbarrios)
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from paid.core.debugger import AIDebugger, debug_with_ai


def test_division_by_zero():
    """Test division by zero error detection"""
    print("\n" + "="*70)
    print("TEST 1: Division by Zero")
    print("="*70 + "\n")
    
    code = """
def divide(a, b):
    return a / b

result = divide(10, 0)
"""
    
    debugger = AIDebugger(api_key="Unused")
    result = debugger.debug_code(code)
    assert result is not None, "Should detect division by zero error"
    print("✅ TEST PASSED: Division by zero error detected and explained")


def test_index_error():
    """Test list index out of range error"""
    print("\n" + "="*70)
    print("TEST 2: Index Out of Range")
    print("="*70 + "\n")
    
    code = """
numbers = [1, 2, 3]
value = numbers[10]
"""
    
    result = debug_with_ai(code, api_key="Unused")
    assert result is not None, "Should detect index error"
    print("✅ TEST PASSED: Index error detected and explained")


def test_type_error():
    """Test type error detection"""
    print("\n" + "="*70)
    print("TEST 3: Type Error")
    print("="*70 + "\n")
    
    code = """
age = "25"
next_year = age + 1
"""
    
    result = debug_with_ai(code, api_key="Unused")
    assert result is not None, "Should detect type error"
    print("✅ TEST PASSED: Type error detected and explained")


def test_key_error():
    """Test dictionary key error"""
    print("\n" + "="*70)
    print("TEST 4: Key Error")
    print("="*70 + "\n")
    
    code = """
data = {"name": "John"}
email = data["email"]
"""
    
    result = debug_with_ai(code, api_key="Unused")
    assert result is not None, "Should detect key error"
    print("✅ TEST PASSED: Key error detected and explained")


def test_name_error():
    """Test undefined variable error"""
    print("\n" + "="*70)
    print("TEST 5: Name Error")
    print("="*70 + "\n")
    
    code = """
def greet():
    print(f"Hello {undefined_variable}")

greet()
"""
    
    result = debug_with_ai(code, api_key="Unused")
    assert result is not None, "Should detect name error"
    print("✅ TEST PASSED: Name error detected and explained")


def test_successful_code():
    """Test that valid code runs without errors"""
    print("\n" + "="*70)
    print("TEST 6: Valid Code (Should Pass)")
    print("="*70 + "\n")
    
    code = """
numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
print(f"Total: {total}")
"""
    
    debugger = AIDebugger(api_key="Unused")
    result = debugger.debug_code(code)
    assert result is None, "Should not detect any error"
    print("✅ TEST PASSED: Valid code executed successfully")


def run_all_tests():
    """Run all test cases"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║  🧪 AI Debugger Test Suite                               ║
    ║  Author: Eduardo J. Barrios (github.com/edujbarrios)     ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    tests = [
        test_division_by_zero,
        test_index_error,
        test_type_error,
        test_key_error,
        test_name_error,
        test_successful_code
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ TEST FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ TEST ERROR: {e}")
            failed += 1
        
        input("\nPress Enter to continue to next test...")
    
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📊 Total: {passed + failed}")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_all_tests()
