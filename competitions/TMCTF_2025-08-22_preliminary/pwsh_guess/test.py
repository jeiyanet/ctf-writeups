import re

# Load the file
with open("power.sh", "r") as f:
    data = f.read()

# Regex to find all hex patterns like 0x41, 0x6A, etc.
hex_pattern = re.compile(r'0x([0-9A-Fa-f]{2})')

# Function to convert a hex match to ASCII
def hex_to_ascii(match):
    hex_value = match.group(1)           # Get the hex digits after 0x
    ascii_char = chr(int(hex_value, 16)) # Convert hex to integer, then to ASCII
    return ascii_char

# Replace all hex patterns in the file with their ASCII equivalent
converted_data = hex_pattern.sub(hex_to_ascii, data)

# Save or print the result
with open("converted_file.txt", "w") as f:
    f.write(converted_data)

print("Conversion complete!")
