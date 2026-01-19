import json
import os
import sys

# Ensure the parent directory is in sys.path
sys.path.append(os.getcwd())

from src.main import app

def generate_openapi():
    # Ensure docs directory exists
    os.makedirs("docs", exist_ok=True)
    
    openapi_schema = app.openapi()
    
    output_path = "docs/openapi.json"
    with open(output_path, "w") as f:
        json.dump(openapi_schema, f, indent=2)
    print(f"✅ Generated {output_path}")

if __name__ == "__main__":
    generate_openapi()