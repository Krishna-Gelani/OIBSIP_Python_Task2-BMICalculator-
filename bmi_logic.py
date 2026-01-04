import math

def calculate_bmi(weight_kg, height_m):
    """
    Calculates BMI using the formula: BMI = weight / (height^2)
    
    Args:
        weight_kg (float): Weight in kilograms.
        height_m (float): Height in meters.
        
    Returns:
        float: Calculated BMI value.
        
    Raises:
        ValueError: If inputs are not positive numbers.
    """
    if weight_kg <= 0 or height_m <= 0:
        raise ValueError("Weight and height must be positive values.")
    
    return weight_kg / (height_m ** 2)

def categorize_bmi(bmi):
    """
    Categorizes the BMI value into standard ranges.
    
    Args:
        bmi (float): The BMI value.
        
    Returns:
        str: Category name.
    """
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi <= 24.9:
        return "Normal"
    elif 25 <= bmi <= 29.9:
        return "Overweight"
    else:
        return "Obese"

def validate_input(weight_str, height_str):
    """
    Validates the user input.
    
    Args:
        weight_str (str): Input weight string.
        height_str (str): Input height string.
        
    Returns:
        tuple: (weight, height) as floats if valid.
        
    Raises:
        ValueError: If inputs are invalid numbers or unrealistic ranges.
    """
    try:
        weight = float(weight_str)
        height = float(height_str)
    except ValueError:
        raise ValueError("Inputs must be numeric values.")

    if not (1 < weight < 600): # World record heavy is ~635kg
        raise ValueError("Please enter a realistic weight (1kg - 600kg).")
    
    if not (0.5 < height < 3.0): # World record tall is ~2.72m
        raise ValueError("Please enter a realistic height (0.5m - 3.0m).")
        
    return weight, height
