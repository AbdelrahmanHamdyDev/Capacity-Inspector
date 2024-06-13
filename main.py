import os
import psutil
import shutil
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

def Get_Drivers():
  drives = []
  type = []
  partitions = psutil.disk_partitions()
  for partition in partitions:
    drives.append(partition.device.replace("\\", "/"))
    type.append(partition.fstype)
  return drives,type

def format_Driver(drive_letter,drive_type):
  print("--> Formatting")
  format_command = f'powershell.exe -Command "Format-Volume -DriveLetter {drive_letter} -FileSystem {drive_type} -Confirm:$false -ErrorAction SilentlyContinue'
  os.system(format_command)

def Create_file(path):
  print("--> Checking")
  os.makedirs(path, exist_ok=True)

  file_size = 1 * 1024 * 1024  # 1 MB in bytes
  file_name = "sample.hamdy"
  # Write zeros to the file
  with open(path + file_name, "wb") as f:
    f.write(bytearray(file_size))

def Duplicate_file(path,total_files):
  counter = 0
  try:
    for i in tqdm(range(int(total_files))):
      counter = i
      duplicate_file = f"sample{i}.hamdy"
      shutil.copyfile(f"{path}sample.hamdy", path+duplicate_file)
  except:
    pass
  return counter

def delete_files(path):
  print("--> Stock Again")
  os.remove(path)

def main():

  drivers, types = Get_Drivers()
  print("  ".join(f"{index}: '{element}'" for index, element in enumerate(drivers)))

  try:
    Index = int(input("choose number: "))
    if (Index >= len(drivers)):
      raise ValueError("LOOL")
  except:
    print("Enter Valed Number!!")
    main()

  type = types[Index]
  Letter = drivers[Index]
  format_Driver(Letter, type)

  usage = psutil.disk_usage(Letter)

  path = Letter + "CapacityInspector_testfiles/"
  Create_file(path)

  counter = Duplicate_file(path, usage.total / (1024 * 1024))
  print(f"Approximate capacity = '{counter / 1024:.2f}GB'")

  delete_files(path)
  input("Press Enter to exit...")

main()