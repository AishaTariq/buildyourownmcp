"""
Enhanced Calculator MCP Server - Scenario 3
Builds on Scenario 2 by adding Prompts and Resources

This demonstrates:
- Tools: Basic calculator operations + storage functions
- Prompts: Guided multi-step calculations
- Resources: Constants, formulas, and stored values
"""

from fastmcp import FastMCP
import json
from typing import Dict, Any
import math

# Create MCP server
mcp = FastMCP(name="Enhanced Calculator")

# In-memory storage for user values
stored_values: Dict[str, float] = {}


# ============================================================================
# TOOLS - Calculator Operations
# ============================================================================

@mcp.tool()
def add(a: float, b: float) -> dict:
    """Add two numbers.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        dict: Result of addition
    """
    result = a + b
    return {"operation": "add", "result": result}


@mcp.tool()
def subtract(a: float, b: float) -> dict:
    """Subtract two numbers.
    
    Args:
        a: First number
        b: Second number (subtracted from a)
    
    Returns:
        dict: Result of subtraction
    """
    result = a - b
    return {"operation": "subtract", "result": result}


@mcp.tool()
def multiply(a: float, b: float) -> dict:
    """Multiply two numbers.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        dict: Result of multiplication
    """
    result = a * b
    return {"operation": "multiply", "result": result}


@mcp.tool()
def divide(a: float, b: float) -> dict:
    """Divide two numbers.
    
    Args:
        a: Numerator
        b: Denominator
    
    Returns:
        dict: Result of division or error message
    """
    if b == 0:
        return {"operation": "divide", "error": "Cannot divide by zero"}
    result = a / b
    return {"operation": "divide", "result": result}


@mcp.tool()
def power(base: float, exponent: float) -> dict:
    """Raise a number to a power.
    
    Args:
        base: The base number
        exponent: The exponent
    
    Returns:
        dict: Result of exponentiation
    """
    result = base ** exponent
    return {"operation": "power", "result": result}


@mcp.tool()
def square_root(number: float) -> dict:
    """Calculate the square root of a number.
    
    Args:
        number: The number to find the square root of
    
    Returns:
        dict: Square root result or error
    """
    if number < 0:
        return {"operation": "square_root", "error": "Cannot calculate square root of negative number"}
    result = math.sqrt(number)
    return {"operation": "square_root", "result": result}


@mcp.tool()
def percentage(value: float, total: float) -> dict:
    """Calculate what percentage one number is of another.
    
    Args:
        value: The part/value
        total: The whole/total
    
    Returns:
        dict: Percentage result
    """
    if total == 0:
        return {"operation": "percentage", "error": "Total cannot be zero"}
    result = (value / total) * 100
    return {"operation": "percentage", "result": result}



# ============================================================================
# TOOLS - Storage Functions (NEW!)
# ============================================================================

@mcp.tool()
def store_number(name: str, value: float) -> dict:
    """Store a number with a name for later use.
    
    Args:
        name: Variable name to store (e.g., 'revenue', 'pi', 'tax_rate')
        value: The numeric value to store
    
    Returns:
        dict: Confirmation message
    """
    stored_values[name] = value
    return {
        "status": "success",
        "message": f"Stored '{name}' = {value}",
        "stored_count": len(stored_values)
    }


@mcp.tool()
def get_stored_number(name: str) -> dict:
    """Retrieve a previously stored number.
    
    Args:
        name: Variable name to retrieve
    
    Returns:
        dict: The stored value or error message
    """
    if name in stored_values:
        return {
            "name": name,
            "value": stored_values[name],
            "status": "found"
        }
    return {
        "name": name,
        "status": "not_found",
        "error": f"No stored value found for '{name}'. Use list_stored_numbers to see available values."
    }


@mcp.tool()
def list_stored_numbers() -> dict:
    """List all currently stored numbers.
    
    Returns:
        dict: All stored values and count
    """
    return {
        "stored_values": stored_values,
        "count": len(stored_values),
        "message": "Use get_stored_number(name) to retrieve a specific value"
    }


@mcp.tool()
def clear_storage() -> dict:
    """Clear all stored numbers.
    
    Returns:
        dict: Confirmation message
    """
    count = len(stored_values)
    stored_values.clear()
    return {
        "status": "success",
        "message": f"Cleared {count} stored value(s)",
        "stored_values": {}
    }


@mcp.tool()
def teradata_secret_message():
    """Returns a special message for demo attendees."""
    return "🎓 Thank you for joining us today for this training session! We hope you had a great learning experience, signing off!"



# ============================================================================
# PROMPTS - Guided Calculation Workflows (NEW!)
# ============================================================================

@mcp.prompt()
def calculate_profit_margin() -> str:
    """Guide the user through calculating profit margin percentage.
    
    Profit Margin = ((Revenue - Costs) / Revenue) × 100
    """
    return """I'll help you calculate profit margin.

Please provide:
1. Total Revenue
2. Total Costs

I will:
1. Use subtract(revenue, costs) to get profit
2. Use divide(profit, revenue) to get the margin as decimal
3. Use multiply(result, 100) to convert to percentage

The formula is: Profit Margin = ((Revenue - Costs) / Revenue) × 100

You can also store values using store_number() for easy reuse!"""


# ============================================================================
# RESOURCES - Stored Values, history, constants
# ============================================================================


@mcp.resource("calculator://stored-values")
def get_stored_values() -> str:
    """Access all currently stored values."""
    if not stored_values:
        return "# Stored Values\n\nNo values stored yet.\n\n💡 Use store_number(name, value) to save values for later use."
    
    output = "# Stored Values\n\n"
    output += f"Total stored: {len(stored_values)}\n\n"
    
    for name, value in sorted(stored_values.items()):
        output += f"- **{name}**: {value}\n"
    
    output += "\n💡 Use get_stored_number(name) to retrieve a value\n"
    output += "💡 Use list_stored_numbers() to see all values as JSON"
    
    return output


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Run with STDIO transport (for local testing)
    # Change to transport="http" for deployment
    mcp.run(transport="http")
