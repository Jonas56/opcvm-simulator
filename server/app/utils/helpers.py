"""
Utility helper functions.
"""

import re
from typing import Optional


def validate_fund_name(fund_name: str) -> bool:
    """
    Validate fund name format.
    
    Args:
        fund_name: Fund name to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not fund_name or not isinstance(fund_name, str):
        return False
    
    # Check for basic format (letters, numbers, spaces, hyphens)
    pattern = r'^[A-Za-z0-9\s\-]+$'
    return bool(re.match(pattern, fund_name))


def format_currency(amount: float, currency: str = "MAD") -> str:
    """
    Format currency amount.
    
    Args:
        amount: Amount to format
        currency: Currency code
        
    Returns:
        Formatted currency string
    """
    return f"{amount:,.2f} {currency}"


def calculate_percentage_change(initial: float, final: float) -> float:
    """
    Calculate percentage change between two values.
    
    Args:
        initial: Initial value
        final: Final value
        
    Returns:
        Percentage change as decimal
    """
    if initial == 0:
        return 0.0
    return ((final - initial) / initial) * 100


def sanitize_string(text: str) -> str:
    """
    Sanitize string input.
    
    Args:
        text: Text to sanitize
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    sanitized = re.sub(r'\s+', ' ', text.strip())
    return sanitized
