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

# Calculation history (last 10 operations)
calculation_history = []


# ============================================================================
# TOOLS - Calculator Operations (from Scenario 2)
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
    _add_to_history("add", a, b, result)
    return {"operation": "add", "result": result, "expression": f"{a} + {b} = {result}"}


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
    _add_to_history("subtract", a, b, result)
    return {"operation": "subtract", "result": result, "expression": f"{a} - {b} = {result}"}


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
    _add_to_history("multiply", a, b, result)
    return {"operation": "multiply", "result": result, "expression": f"{a} × {b} = {result}"}


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
    _add_to_history("divide", a, b, result)
    return {"operation": "divide", "result": result, "expression": f"{a} ÷ {b} = {result}"}


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
def power(base: float, exponent: float) -> dict:
    """Raise a number to a power.
    
    Args:
        base: The base number
        exponent: The exponent
    
    Returns:
        dict: Result of exponentiation
    """
    result = base ** exponent
    _add_to_history("power", base, exponent, result)
    return {"operation": "power", "result": result, "expression": f"{base}^{exponent} = {result}"}


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
    return {"operation": "square_root", "result": result, "expression": f"√{number} = {result}"}


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
    return {
        "operation": "percentage",
        "result": result,
        "expression": f"{value} is {result}% of {total}"
    }

@mcp.tool()
def teradata_secret_message():
    """Returns a special message for demo attendees."""
    return "🎓 Thank you for joining us for this demo! Keep learning with Teradata University! (Local)"



# ============================================================================
# PROMPTS - Guided Calculation Workflows (NEW!)
# ============================================================================

@mcp.prompt()
def calculate_compound_interest() -> str:
    """Guide the user through calculating compound interest.
    
    This prompt helps calculate: A = P(1 + r/n)^(nt)
    Where:
    - P = Principal (initial amount)
    - r = Annual interest rate (as decimal)
    - n = Times interest is compounded per year
    - t = Time in years
    """
    return """I'll help you calculate compound interest step by step.

Please provide:
1. Principal amount (initial investment)
2. Annual interest rate (as a percentage, e.g., 5 for 5%)
3. Compounding frequency per year (e.g., 12 for monthly, 4 for quarterly, 1 for annual)
4. Time period in years

Formula: A = P(1 + r/n)^(nt)

After you provide these values, I'll:
1. Convert the percentage rate to decimal (divide by 100)
2. Calculate r/n
3. Add 1 to that result
4. Calculate nt (n × t)
5. Raise to the power
6. Multiply by principal

Use the calculator tools (divide, add, multiply, power) to compute each step."""


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


@mcp.prompt()
def convert_units() -> str:
    """Guide the user through unit conversion calculations.
    
    Uses stored conversion factors from resources.
    """
    return """I'll help you convert between units.

Common conversions available in calculator://conversion-factors:
- Length: inches ↔ cm, miles ↔ km, feet ↔ meters
- Weight: pounds ↔ kg, ounces ↔ grams
- Temperature: Fahrenheit ↔ Celsius
- Volume: gallons ↔ liters

Steps:
1. Tell me what unit conversion you need
2. I'll retrieve the conversion factor from resources
3. Use multiply() or divide() to convert

Example: "Convert 10 miles to kilometers"
- I'll get the factor (1.60934) from resources
- Then multiply(10, 1.60934) = 16.0934 km"""


@mcp.prompt()
def financial_analysis() -> str:
    """Guide through common financial calculations for business analysis.
    
    Includes ROI, break-even analysis, and growth rates.
    """
    return """I'll help with financial analysis calculations.

Available analyses:
1. **ROI (Return on Investment)**: ((Gain - Cost) / Cost) × 100
2. **Break-Even Point**: Fixed Costs / (Price - Variable Cost per Unit)
3. **Growth Rate**: ((New Value - Old Value) / Old Value) × 100
4. **Compound Annual Growth Rate (CAGR)**: ((Ending/Beginning)^(1/years) - 1) × 100

Tell me which analysis you need and provide the required values.

Pro tip: Use store_number() to save quarterly or annual figures, then reference them by name!

Example:
- store_number('q1_revenue', 100000)
- store_number('q2_revenue', 125000)
- Then calculate growth between quarters"""


# ============================================================================
# RESOURCES - Constants, Formulas, and Data (NEW!)
# ============================================================================

@mcp.resource("calculator://constants")
def get_math_constants() -> str:
    """Mathematical constants for calculations."""
    constants = {
        "pi": math.pi,
        "e": math.e,
        "golden_ratio": 1.618033988749895,
        "sqrt_2": math.sqrt(2),
        "sqrt_3": math.sqrt(3),
        "euler_mascheroni": 0.5772156649015329
    }
    
    output = "# Mathematical Constants\n\n"
    for name, value in constants.items():
        output += f"**{name}**: {value}\n"
    
    output += "\n💡 Tip: Use these in calculations by referencing the value directly, "
    output += "or store them with store_number() for easy access."
    
    return output


@mcp.resource("calculator://conversion-factors")
def get_conversion_factors() -> str:
    """Unit conversion factors."""
    conversions = {
        "Length": {
            "inches_to_cm": 2.54,
            "feet_to_meters": 0.3048,
            "miles_to_km": 1.60934,
            "yards_to_meters": 0.9144
        },
        "Weight": {
            "pounds_to_kg": 0.453592,
            "ounces_to_grams": 28.3495,
            "tons_to_kg": 907.185
        },
        "Volume": {
            "gallons_to_liters": 3.78541,
            "quarts_to_liters": 0.946353,
            "cups_to_ml": 236.588
        },
        "Temperature": {
            "note": "F to C: (F - 32) × 5/9",
            "note2": "C to F: (C × 9/5) + 32"
        }
    }
    
    output = "# Unit Conversion Factors\n\n"
    for category, factors in conversions.items():
        output += f"## {category}\n"
        for name, value in factors.items():
            if isinstance(value, (int, float)):
                output += f"- **{name}**: {value}\n"
            else:
                output += f"- *{value}*\n"
        output += "\n"
    
    output += "💡 To convert: multiply(value, conversion_factor)\n"
    output += "💡 To reverse: divide(value, conversion_factor)"
    
    return output


@mcp.resource("calculator://formulas")
def get_common_formulas() -> str:
    """Common mathematical and financial formulas."""
    formulas = {
        "Financial": [
            "**Profit Margin**: ((Revenue - Costs) / Revenue) × 100",
            "**ROI**: ((Gain - Cost) / Cost) × 100",
            "**Compound Interest**: A = P(1 + r/n)^(nt)",
            "**Simple Interest**: I = P × r × t",
            "**Break-Even**: Fixed Costs / (Price - Variable Cost)"
        ],
        "Geometric": [
            "**Circle Area**: π × r²",
            "**Circle Circumference**: 2 × π × r",
            "**Rectangle Area**: length × width",
            "**Triangle Area**: (base × height) / 2",
            "**Sphere Volume**: (4/3) × π × r³"
        ],
        "Statistical": [
            "**Mean**: sum / count",
            "**Percentage Change**: ((New - Old) / Old) × 100",
            "**Percentage of Total**: (Part / Total) × 100",
            "**Weighted Average**: Σ(value × weight) / Σ(weights)"
        ]
    }
    
    output = "# Common Formulas\n\n"
    for category, formula_list in formulas.items():
        output += f"## {category}\n"
        for formula in formula_list:
            output += f"- {formula}\n"
        output += "\n"
    
    output += "💡 Use the calculator tools to compute these step by step!\n"
    output += "💡 Use the prompts for guided calculations of complex formulas."
    
    return output


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


@mcp.resource("calculator://history")
def get_calculation_history() -> str:
    """View recent calculation history."""
    if not calculation_history:
        return "# Calculation History\n\nNo calculations performed yet."
    
    output = "# Calculation History\n\n"
    output += f"Last {len(calculation_history)} calculation(s):\n\n"
    
    for i, calc in enumerate(reversed(calculation_history), 1):
        output += f"{i}. **{calc['operation']}**: {calc['expression']} = {calc['result']}\n"
    
    return output


# ============================================================================
# Helper Functions
# ============================================================================

def _add_to_history(operation: str, a: float, b: float, result: float):
    """Add a calculation to history (keep last 10)."""
    expression = f"{a} {_get_operator_symbol(operation)} {b}"
    calculation_history.append({
        "operation": operation,
        "expression": expression,
        "result": result
    })
    
    # Keep only last 10
    if len(calculation_history) > 10:
        calculation_history.pop(0)


def _get_operator_symbol(operation: str) -> str:
    """Get the mathematical symbol for an operation."""
    symbols = {
        "add": "+",
        "subtract": "-",
        "multiply": "×",
        "divide": "÷",
        "power": "^"
    }
    return symbols.get(operation, operation)


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    # Run with STDIO transport (for local testing)
    # Change to transport="http" for deployment
    mcp.run(transport="http")
