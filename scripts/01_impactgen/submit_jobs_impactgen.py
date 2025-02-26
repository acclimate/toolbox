import os
import subprocess
# by Kilian Kuhla
# Define the start and final years
years_ssp = [(2019 + 10 * i, 2019 + 10 * i + 10) for i in range(8)]
years = {
  'ssp126': years_ssp,
  'ssp370': years_ssp,
  'ssp585': years_ssp,
  'observation': [(1980 + 10 * i, 1980 + 10 * i + 9) for i in range(4)]
}

# Set up directories
scenario_dir = "/p/projects/acclimate/projects/heated_productivity/settings/impactgen_settings"
impact_dir = "/home/kikuhla/Documents/impactgen/build/"
input_data_dir = "/p/projects/dfg_health_africa/data/ISIMIP3b/global"
output_data_dir = "/p/projects/acclimate/projects/heated_productivity/data/input/forcing"
log_dir = "/p/tmp/kikuhla/data/log"

os.makedirs(log_dir, exist_ok=True)

# Define the SSPs and GCM models
ssps = ['ssp126', 'ssp370', 'ssp585', 'observation']
gcm_models = [
  'CanESM5', 'CNRM-CM6-1', 'CNRM-ESM2-1', 'EC-Earth3', 'GFDL-ESM4',
  'IPSL-CM6A-LR', 'MIROC6', 'MPI-ESM1-2-HR', 'MRI-ESM2-0', 'UKESM1-0-LL'
]

def give_running_name(ssp, gcm, wanted_years):
  """Generate a running name for the job."""
  return f"{ssp}_{gcm.lower()}_{wanted_years[0]}-{wanted_years[1]}"

def create_yml(ssp, gcm, wanted_years, name):
  """Create the YAML script content."""
  if ssp == 'observation':
    productivity_file = (
      "/p/projects/acclimate/kilian/data/input/heated_productivity/"
      "ISIMIP3b/observation/WFDE5_v2.0/day/observation_wfde5_v2.0_[[year]].nc"
    )
  else:
    if gcm in ['CNRM-CM6-1', 'CNRM-ESM2-1', 'UKESM1-0-LL']:
      productivity_file = (
        f"{input_data_dir}/{ssp}/{gcm}/day/{gcm.lower()}_r1i1p1f2_w5e5_"
        f"{ssp}_dayavg_productivity_global_day_[[year]].nc"
      )
    else:
      productivity_file = (
        f"{input_data_dir}/{ssp}/{gcm}/day/{gcm.lower()}_r1i1p1f1_w5e5_"
        f"{ssp}_dayavg_productivity_global_day_[[year]].nc"
      )
  yml_script = f"""combination: addition
reference: days since {wanted_years[0]}-01-01
regions:
  type: netcdf
  file: /p/projects/acclimate/data/eora/EORA2015_CHN_USA.nc
  variable: region
sectors:
  type: netcdf
  file: /p/projects/acclimate/data/eora/EORA2015_CHN_USA.nc
  variable: sector
output:
  file: {output_data_dir}/{ssp}/impacts_{name}.nc
impacts:
  - type: heated_productivity
  chunk_size: 25
  worker_categories:
    - name: sectors_200W
    sectors:
      - WHOT
      - RETT
      - GAST
      - TRAN
      - GAST
      - COMM
      - FINC
      - ADMI
      - EDHE
      - HOUS
      - OTHE
      - REXI
    - name: sectors_300W
    sectors:
      - OILC
      - FOOD
      - WOOD
      - METL
      - MACH
      - TREQ
      - MANU
      - RECY
      - ELWA
      - REPA
      - TEXL
    - name: sectors_400W
    sectors:
      - AGRI
      - FISH
      - MINQ
      - CONS
  isoraster:
    file: /p/projects/acclimate/kilian/data/input/raster/iso_raster_adv_CHN_USA_1800_sec.nc
    variable: iso
  proxy:
    file: /p/projects/acclimate/data/population/gpw/gpw_v4_population_count_rev11_2015_1800_sec_remapped.nc
    variable: Band1
  heated_productivity:
    file: {productivity_file}
    variable: dayavg_productivity
  variables:
    year:
    from: {wanted_years[0]}
    to: {wanted_years[1]}
  time_shift: 0
"""
  return yml_script

def create_job_script(name, ssp):
  """Create the job script content."""
  job_script = f"""#!/bin/sh
#SBATCH --job-name='impactgen_{name}'
#SBATCH --partition=standard
#SBATCH --qos=short
#SBATCH --time=00:30:00
#SBATCH --error={log_dir}/errors-%j.txt
#SBATCH --export=ALL
#SBATCH --mail-type=FAIL,END
#SBATCH --mail-user=kikuhla@pik-potsdam.de  
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --chdir={log_dir}
export OMP_PROC_BIND=true
export OMP_NUM_THREADS=1

module load gcc/13.2.0
module load netcdf-c/4.9.2

{impact_dir}/impactgen {scenario_dir}/setting_{name}.yml

source activate compacts-simulations
python3 /p/projects/acclimate/projects/heated_productivity/scripts/add_one_to_impact_file.py {output_data_dir}/{ssp}/impacts_{name}.nc {output_data_dir}/{ssp}/impacts_{name}_preday.nc
"""
  return job_script

a = 0
for ssp in ssps:
  for gcm in gcm_models:
    if ssp == 'observation' and a == 1:
      continue
    elif ssp == 'observation' and a == 0:
      gcm = 'None'
      a = 1
    for wanted_years in years[ssp]:
      # Create YAML script
      running_name = give_running_name(ssp, gcm, wanted_years)
      yml_script_content = create_yml(ssp, gcm, wanted_years, running_name)
      yml_script_path = f"{scenario_dir}/setting_{running_name}.yml"
      with open(yml_script_path, "w") as f:
        f.write(yml_script_content)
      
      # Create job script
      job_script_content = create_job_script(running_name, ssp)
      job_script_path = f"{log_dir}/job_{running_name}.job"
      with open(job_script_path, "w") as f:
        f.write(job_script_content)

      if subprocess.check_output(["squeue", "-u", "kikuhla", "-n", f"{running_name}", "--noheader", "--format=%A"]).decode("utf-8") == '':
        subprocess.run(["sbatch", job_script_path])
      else:
        print(f"{running_name}: Equivalent Job is already running!")

exit()