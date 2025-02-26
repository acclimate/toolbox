''' This script partitions the list of settings file for the ensemble simulations,
removes settings files not to be used, 
and selects specific decade, in this example the next few decades. 
'''

import ruamel.yaml as yaml
import os
file = "/p/projects/acclimate/projects/heated_productivity/settings/acclimate_settings/settings_example_ensemble.yml"

# Load the settings file
with open(os.path.join(file), "r") as file:
    yaml_readr = yaml.YAML()
    yaml_readr.indent(sequence=4, offset=2)
    settingslist = yaml_readr.load(file)


#remove all list entries containing 2010,2020,2030,2040,2050,2060,2070,2080,2090,2100...
years_to_remove = [str(year) for year in range(1940, 2111, 10)]

def remove_years_from_list(settings_list):
    return [item for item in settings_list if not any(year in item for year in years_to_remove)]

new_settingslist = []
for file in settingslist:
    if not any(year in file for year in years_to_remove):
        new_settingslist.append(file)
        
#select specific decades

#only select settings up to 2050
next_decades = [file for file in new_settingslist if not any(year in file for year in [str(year) for year in range(2059, 2111, 10)])]


# Save the updated settings list to a new YAML file
new_file = "/p/projects/acclimate/projects/heated_productivity/settings/acclimate_settings/settings_next_decades.yml"
with open(new_file, "w") as file:
    yaml_readr = yaml.YAML()
    yaml_readr.indent(sequence=4, offset=2)
    yaml_readr.dump(next_decades, file)