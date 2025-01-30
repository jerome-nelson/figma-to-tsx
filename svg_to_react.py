import os

SVG_DIRECTORY = "generated/svgs"
TSX_DIRECTORY = "generated/tsx"

def snake_to_pascal(snake_str):
    return ''.join(word.capitalize() for word in snake_str.split('_'))


# Function to convert SVG to JSX
def svg_to_jsx(svg_file, jsx_file_name):
    
    with open(svg_file, "r") as file:
        content = file.read()

    # Create the JSX content
    jsx_content = "import React from 'react';\n\n"
    jsx_content += f"const {snake_to_pascal(jsx_file_name)}: React.FC = (props) => (\n"
    jsx_content += content.replace('<svg', '<svg {...props}')

    # Convert SVG attributes to JSX attributes
   
    jsx_content += ");\n\n"
    jsx_content += f"export default {snake_to_pascal(jsx_file_name)};"

    # Write the JSX content to a file
    with open(f"{TSX_DIRECTORY}/{jsx_file_name}.tsx", "w") as jsx_file:
        jsx_file.write(jsx_content)

    print(f"⚛️ TSX component saved as {TSX_DIRECTORY}/{jsx_file_name}.tsx")

# Function to scan directory and process all SVG files
def generate_jsx_from_svgs():
    # Check if the directory exists
    if not os.path.exists(SVG_DIRECTORY):
        print(f"Directory {SVG_DIRECTORY} does not exist!")
        return
    
    # Create the JSX Directory if it doesn't exist
    os.makedirs(TSX_DIRECTORY, exist_ok=True)
    
    # Scan the directory for SVG files
    for file_name in os.listdir(SVG_DIRECTORY):
        # Process only SVG files
        if file_name.endswith(".svg"):
            svg_file_path = os.path.join(SVG_DIRECTORY, file_name)
            # Generate a React component name from the SVG file name (strip the ".svg" extension)
            jsx_file_name = file_name.replace(".svg", "")
            # Call the svg_to_jsx function
            svg_to_jsx(svg_file_path, jsx_file_name)

