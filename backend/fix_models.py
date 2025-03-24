# Create this as backend/fix_models.py
import os

# Game model file path
game_model_path = os.path.join('app', 'models', 'game.py')

# Read the existing file
with open(game_model_path, 'r') as file:
    content = file.read()

# Replace the problematic relationship line
if 'simulations = relationship("Simulation"' in content:
    fixed_content = content.replace(
        'simulations = relationship("Simulation"', 
        'simulations = relationship("Simulation", backref="game", lazy="dynamic"'
    )
    
    # Write the fixed content
    with open(game_model_path, 'w') as file:
        file.write(fixed_content)
    print("Fixed Game model relationship")
else:
    print("No changes needed or different format found")