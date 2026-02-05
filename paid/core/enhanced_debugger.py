"""
Enhanced AI Debugger with Jinja2 Template Support
Author: Eduardo J. Barrios (github.com/edujbarrios)
Uses llm7.io for intelligent error analysis
"""

import sys
import traceback
import openai
from typing import Optional, Dict, Any
import json

# Try to import Jinja2, fall back to basic formatting if not available
try:
    from ..utils.prompt_templates import render_error_prompt, get_system_prompt
    JINJA2_AVAILABLE = True
except (ImportError, ValueError):
    JINJA2_AVAILABLE = False


class AIDebugger:
    """
    Intelligent debugger that captures Python errors and provides
    human-readable explanations using AI with Jinja2 template support.
    """
    
    def __init__(self, api_key: str = "Unused", use_templates: bool = True):
        """
        Initialize the AI Debugger.
        
        Args:
            api_key: Your llm7.io API key (get it free at https://token.llm7.io/)
            use_templates: Whether to use Jinja2 templates (if available)
        """
        self.client = openai.OpenAI(
            base_url="https://api.llm7.io/v1",
            api_key=api_key
        )
        self.use_templates = use_templates and JINJA2_AVAILABLE
        
    def format_error_context(self, error_info: Dict[str, Any], template: str = "standard") -> str:
        """
        Format error information for AI analysis using Jinja2 templates.
        
        Args:
            error_info: Dictionary containing error details
            template: Template type (currently only 'standard' is used)
            
        Returns:
            Formatted string ready for AI processing
        """
        if self.use_templates:
            return render_error_prompt(
                code=error_info['code'],
                error_type=error_info['error_type'],
                error_message=error_info['error_message'],
                traceback=error_info['traceback'],
                file_path=error_info.get('file_path', ''),
                line_number=error_info.get('line_number', '')
            )
        else:
            # Fallback to basic formatting
            return f"""
You are an expert Python debugger. Analyze this error:

SOURCE CODE:
{error_info['code']}

ERROR INFORMATION:
Type: {error_info['error_type']}
Message: {error_info['error_message']}

TRACEBACK:
{error_info['traceback']}

Provide a clear explanation covering:
1. What happened
2. Where it occurs
3. Why it occurs
4. How to fix it
5. Best practices to avoid this

Be direct and educational.
"""

    def analyze_error(self, 
                     code: str, 
                     error_type: str,
                     error_message: str,
                     traceback_str: str,
                     model: str = "default",
                     template: str = "standard") -> str:
        """
        Send error to AI for analysis and get human-readable explanation.
        
        Args:
            code: The source code that caused the error
            error_type: Type of exception (e.g., 'ValueError', 'TypeError')
            error_message: The error message
            traceback_str: Full traceback string
            model: AI model to use ('default', 'fast', or 'pro')
            template: Template type ('standard', 'detailed', or 'quick')
            
        Returns:
            AI-generated explanation of the error
        """
        error_info = {
            'code': code,
            'error_type': error_type,
            'error_message': error_message,
            'traceback': traceback_str
        }
        
        prompt = self.format_error_context(error_info, template)
        system_prompt = get_system_prompt() if self.use_templates else \
            "You are an expert Python debugger and mentor. Explain errors in clear, simple language following the exact format requested."
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"❌ Error communicating with AI service: {str(e)}"
    
    def debug_code(self, code: str, model: str = "default", template: str = "standard") -> Optional[str]:
        """
        Execute code and capture any errors for AI analysis.
        
        Args:
            code: Python code to execute and debug
            model: AI model to use for analysis
            template: Template type for error formatting
            
        Returns:
            AI explanation if error occurs, None if code runs successfully
        """
        try:
            # Execute the code
            exec(code)
            print("✅ Code executed successfully - no errors detected!")
            return None
            
        except Exception as e:
            # Capture error details
            error_type = type(e).__name__
            error_message = str(e)
            traceback_str = traceback.format_exc()
            
            print("\n" + "="*70)
            print("🔍 ERROR DETECTED - Analyzing with AI...")
            print("="*70 + "\n")
            
            # Get AI analysis
            explanation = self.analyze_error(
                code=code,
                error_type=error_type,
                error_message=error_message,
                traceback_str=traceback_str,
                model=model,
                template=template
            )
            
            print(explanation)
            return explanation
    
    def debug_file(self, filepath: str, model: str = "default", template: str = "standard") -> Optional[str]:
        """
        Read and debug a Python file.
        
        Args:
            filepath: Path to the Python file
            model: AI model to use for analysis
            template: Template type for error formatting
            
        Returns:
            AI explanation if error occurs, None if code runs successfully
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                code = f.read()
            
            print(f"🔍 Debugging file: {filepath}\n")
            return self.debug_code(code, model, template)
            
        except FileNotFoundError:
            print(f"❌ File not found: {filepath}")
            return None
        except Exception as e:
            print(f"❌ Error reading file: {str(e)}")
            return None


def debug_with_ai(code: str, api_key: str = "Unused", model: str = "default", template: str = "standard"):
    """
    Convenience function to quickly debug code with AI.
    
    Args:
        code: Python code to debug
        api_key: Your llm7.io API key
        model: AI model to use ('default', 'fast', or 'pro')
        template: Template type ('standard', 'detailed', or 'quick')
    
    Example:
        >>> code = '''
        ... numbers = [1, 2, 3]
        ... print(numbers[5])
        ... '''
        >>> debug_with_ai(code)
    """
    debugger = AIDebugger(api_key)
    return debugger.debug_code(code, model, template)


# Context manager for automatic error catching
class AutoDebug:
    """
    Context manager that automatically catches and explains errors.
    
    Example:
        >>> with AutoDebug():
        ...     x = 5 / 0
    """
    
    def __init__(self, api_key: str = "Unused", model: str = "default", template: str = "standard"):
        self.debugger = AIDebugger(api_key)
        self.model = model
        self.template = template
        self.code = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            # Get the code that caused the error
            frame = exc_tb.tb_frame
            code_lines = traceback.format_exception(exc_type, exc_val, exc_tb)
            
            error_type = exc_type.__name__
            error_message = str(exc_val)
            traceback_str = ''.join(code_lines)
            
            # Extract relevant code snippet
            code = "Context not available - use debug_code() or debug_file() for full context"
            
            print("\n" + "="*70)
            print("🔍 ERROR DETECTED - Analyzing with AI...")
            print("="*70 + "\n")
            
            explanation = self.debugger.analyze_error(
                code=code,
                error_type=error_type,
                error_message=error_message,
                traceback_str=traceback_str,
                model=self.model,
                template=self.template
            )
            
            print(explanation)
            
            # Suppress the exception (return True)
            return True


if __name__ == "__main__":
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║  🐛 AI-Powered Python Debugger                           ║
    ║  Author: Eduardo J. Barrios (github.com/edujbarrios)     ║
    ║  Powered by llm7.io                                       ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Example usage
    print("\n📝 Example: Debugging inline code\n")
    
    buggy_code = """
numbers = [1, 2, 3, 4, 5]
result = numbers[10]  # Index out of range!
print(result)
"""
    
    debugger = AIDebugger()
    debugger.debug_code(buggy_code)
