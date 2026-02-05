"""
Jinja2 Prompt Template Loader for AI Error Analysis
Author: Eduardo J. Barrios (github.com/edujbarrios)
"""

import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, Template


class PromptTemplateLoader:
    """
    Loads and renders Jinja2 templates from the prompts directory.
    """
    
    def __init__(self):
        """Initialize the template loader with the prompts directory."""
        self.prompts_dir = Path(__file__).parent.parent / 'prompts'
        self.env = Environment(
            loader=FileSystemLoader(str(self.prompts_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def load_template(self, template_name: str) -> Template:
        """
        Load a Jinja2 template from the prompts directory.
        
        Args:
            template_name: Name of the template file (e.g., 'error_analysis.jinja')
        
        Returns:
            Jinja2 Template object
        """
        return self.env.get_template(template_name)
    
    def render_error_analysis(self, code: str, error_type: str, 
                             error_message: str, traceback: str, 
                             **kwargs) -> str:
        """
        Render the main error analysis template.
        
        Args:
            code: The source code that caused the error
            error_type: Type of exception (e.g., 'ValueError')
            error_message: The error message
            traceback: Full traceback string
            **kwargs: Additional template variables
        
        Returns:
            Rendered prompt string
        """
        template = self.load_template('error_analysis.jinja')
        return template.render(
            code=code,
            error_type=error_type,
            error_message=error_message,
            traceback=traceback,
            **kwargs
        )
    
    def load_system_prompt(self) -> str:
        """
        Load the system prompt from file.
        
        Returns:
            System prompt string
        """
        system_prompt_path = self.prompts_dir / 'system_prompt.txt'
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            return f.read().strip()


# Global instance for easy access
_loader = None

def get_loader() -> PromptTemplateLoader:
    """
    Get or create the global template loader instance.
    
    Returns:
        PromptTemplateLoader instance
    """
    global _loader
    if _loader is None:
        _loader = PromptTemplateLoader()
    return _loader


def render_error_prompt(code: str, error_type: str, 
                       error_message: str, traceback: str,
                       **kwargs) -> str:
    """
    Convenience function to render an error analysis prompt.
    
    Args:
        code: The source code that caused the error
        error_type: Type of exception
        error_message: The error message
        traceback: Full traceback string
        **kwargs: Additional template variables
    
    Returns:
        Rendered prompt string
    
    Example:
        >>> prompt = render_error_prompt(
        ...     code='x = [1,2,3]; print(x[5])',
        ...     error_type='IndexError',
        ...     error_message='list index out of range',
        ...     traceback='Traceback...'
        ... )
    """
    loader = get_loader()
    return loader.render_error_analysis(
        code=code,
        error_type=error_type,
        error_message=error_message,
        traceback=traceback,
        **kwargs
    )


def get_system_prompt() -> str:
    """
    Get the system prompt for the AI assistant.
    
    Returns:
        System prompt string
    """
    loader = get_loader()
    return loader.load_system_prompt()
