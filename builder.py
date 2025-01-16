import re
import os

STELLARIS_PATH = "/home/alexchernov/.local/share/Steam/steamapps/common/Stellaris/"

# Adjust Ship Sizes
def adjust_ship_sizes():
  files_to_process = {
    'common/ship_sizes/00_ship_sizes.txt': 'common/ship_sizes/50_ship_sizes.txt',
    'common/ship_sizes/04_fallen_empires.txt': 'common/ship_sizes/50_fallen_empires.txt',
    'common/ship_sizes/08_marauder_ships.txt': 'common/ship_sizes/50_marauder_ships.txt',
    'common/ship_sizes/20_nemesis.txt': 'common/ship_sizes/50_nemesis.txt',
    'common/ship_sizes/25_cosmogenesis.txt': 'common/ship_sizes/50_cosmogenesis.txt',
  }
  # load file contents
  for source_file, target_file in files_to_process.items():
    print(' === Process File: ', source_file)

    content = '# SOURCE: ' + source_file + '\n'
    with open(STELLARIS_PATH + source_file, 'r') as f:
      data = f.read()

    # == Identify ships ==
    matches = re.findall(r'^(\w+) = \{(.+?)^\}', data, re.MULTILINE | re.DOTALL)
    for match in matches:
      ship_name = match[0]
      ship_data = match[1]
      print(' == Ship type: ' + ship_name)

      # replace all "size_multiplier = x" with "size_multiplier = x*10"
      if ship_name in ['titan', 'cosmo_crisis_titan']:
        ship_data = re.sub(r'size_multiplier = (\d+)', r'size_multiplier = 80', ship_data)
      else:
        ship_data = re.sub(r'size_multiplier = (\d+)', r'size_multiplier = \g<1>0', ship_data)
      # add "ship_modifier = { ship_fire_rate_mult = 9 }" before every "size_multiplier" string
      ship_data = re.sub(r'\tsize_multiplier', r'\tship_modifier = {\n\t\tship_fire_rate_mult = 9\n\t\tships_upkeep_mult = 9\n\t}\n\tsize_multiplier', ship_data)
      # increase piracy suppression
      ship_data = re.sub(r'ship_piracy_suppression_add = (\d+)', r'ship_piracy_suppression_add = \g<1>0', ship_data)

      data = data.replace(match[1], ship_data)

    content += data

    # create directories for path if required
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    # save result
    with open(target_file, 'w') as f:
      f.write(content)

# Adjust Component Templates
def adjust_component_templates():
  files_to_process = [
      'common/component_templates/00_utilities_afterburners.txt',
      #'common/component_templates/00_utilities_auras.txt',
      'common/component_templates/00_utilities_aux.txt',
      'common/component_templates/00_utilities_drives.txt',
      'common/component_templates/00_utilities_reactors.txt',
      'common/component_templates/00_utilities_roles.txt',
      'common/component_templates/00_utilities_sensors.txt',
      'common/component_templates/00_utilities_thrusters.txt',
  ]
  for file in files_to_process:
    with open(STELLARIS_PATH + file, 'r') as f:
      data = f.read()
    # replace simple cost declaration
    data = re.sub(r'@cost(\d+) = (\d+)', r'@cost\g<1> = \g<2>0', data)
    # replace ship type cost declaration
    data = re.sub(r'@(\w+)_cost_(\d+) = (\d+)', r'@\g<1>_cost_\g<2> = \g<3>0', data)
    # replace leveled cost
    data = re.sub(r'@cost_L(\d+) = (\d+)', r'@cost_L\g<1> = \g<2>0', data)
    # replace direct alloys cost
    data = re.sub(r'alloys = (\d+)', r'alloys = \g<1>0', data)
    # create path for result file
    os.makedirs(os.path.dirname(file), exist_ok=True)
    # save result
    with open(file, 'w') as f:
      f.write(data)

# Adjust Section Templates
def adjust_section_templates():
  files_to_process = [
    'common/section_templates/corvette.txt',
    'common/section_templates/destroyer.txt',
    'common/section_templates/cruiser.txt',
    'common/section_templates/battleship.txt',
  ]
  for file in files_to_process:
    with open(STELLARIS_PATH + file, 'r') as f:
      data = f.read()
    # replace simple cost declaration
    data = re.sub(r'@section_cost = (\d+)', r'@section_cost = \g<1>0', data)
    os.makedirs(os.path.dirname(file), exist_ok=True)
    # save result
    with open(file, 'w') as f:
      f.write(data)

# Adjust Scripted Variables
def adjust_scripted_variables():
  # COMPONENT COST
  scripted_vars_file = 'common/scripted_variables/02_scripted_variables_component_cost.txt'
  with open(STELLARIS_PATH + scripted_vars_file, 'r') as f:
    data = f.read()
  # replace cost declarations
  data = re.sub(r'@([\w_]+)cost([\w_]*) = (\d+)', r'@\g<1>cost\g<2> = \g<3>0', data)
  os.makedirs(os.path.dirname(scripted_vars_file), exist_ok=True)
  # replace armor declarations
  data = re.sub(r'@armor_(\w*) = (\d+)', r'@armor_\g<1> = \g<2>0', data)
  # replace shield declarations
  data = re.sub(r'@shield_([SML\d]{2}) = (\d+)', r'@shield_\g<1> = \g<2>0', data)
  # save result
  with open(scripted_vars_file, 'w') as f:
    f.write(data)

  # SHIPS
  scripted_vars_file = 'common/scripted_variables/03_scripted_variables_ships.txt'
  with open(STELLARIS_PATH + scripted_vars_file, 'r') as f:
    data = f.read()
  # replace hp declarations
  data = re.sub(r'@(\w+)_hp = (\d+)', r'@\g<1>_hp = \g<2>0', data)
  os.makedirs(os.path.dirname(scripted_vars_file), exist_ok=True)
  # save result
  with open(scripted_vars_file, 'w') as f:
    f.write(data)

adjust_ship_sizes()
# adjust_component_templates()
# adjust_section_templates()
# adjust_scripted_variables()
