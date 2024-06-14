# make py
import glob
import os
import shutil
import subprocess
import sys
import json
import hashlib
import time


### SET CONFIG HERE ###

compiler = " "

compiler_flags = [" "]

linker_flags = [" "]

executable_name = " "




#### Raylib Config ####

# compiler = "g++"

# compiler_flags = ["-std=c++11", "-I./include"]

# linker_flags = ["-L./lib", "-lraylib", "-lopengl32", "-lgdi32", "-lwinmm"]

# executable_name = "game"

#######################



if sys.platform == "win32":
    executable_name += ".exe"

build_dir = "build"
cache_file = os.path.join(build_dir, "makepycache.txt")
os.makedirs(build_dir, exist_ok=True)
cpp_files = glob.glob("src/**/*.cpp", recursive=True)

def check_compiler():
    try:
        subprocess.run([compiler, "--version"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print(f"[ERROR] {compiler} is not found. Please make sure it is installed and available in the system PATH.")
        sys.exit(1)

def load_cache():
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(cache_file, "w") as f:
        json.dump(cache, f)

def get_file_hash(file):
    with open(file, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def compile_file(file, cache, progress):
    obj_file = os.path.join(build_dir, file.replace(".cpp", ".o"))
    os.makedirs(os.path.dirname(obj_file), exist_ok=True)

    if file in cache and cache[file]["hash"] == get_file_hash(file) and os.path.exists(obj_file):
        print(f"skipping {file} [{progress:.2f}%]")
    else:
        print(f"compiling {file} [{progress:.2f}%]")
        subprocess.run([compiler, "-c", file, "-o", obj_file] + compiler_flags, check=True)
        cache[file] = {"hash": get_file_hash(file)}

def compile_files(cpp_files, cache):
    total_files = len(cpp_files)
    for index, file in enumerate(cpp_files, start=1):
        progress = (index / total_files) * 100
        compile_file(file, cache, progress)

def link_files(obj_files):
    print(f"linking {executable_name}")
    subprocess.run([compiler, "-o", os.path.join(build_dir, executable_name)] + obj_files + linker_flags, check=True)

def run_executable():
    executable_path = os.path.abspath(executable_name)
    print(f"running {executable_path}")
    subprocess.run(executable_path)

def main():
    check_compiler()
    cache = load_cache()

    start_time = time.time()

    compile_files(cpp_files, cache)
    obj_files = [os.path.join(build_dir, file.replace(".cpp", ".o")) for file in cpp_files]

    print("\n")

    compile_time = time.time() - start_time
    print(f"compilation time: {compile_time:.2f} seconds")

    start_time = time.time()

    link_files(obj_files)
    shutil.move(os.path.join(build_dir, executable_name), executable_name)

    link_time = time.time() - start_time
    print(f"linking time: {link_time:.2f} seconds")

    print("\n")

    print(f'"{executable_name}" was created')


    save_cache(cache)

    if len(sys.argv) > 1 and sys.argv[1] == "r":
        run_executable()

if __name__ == "__main__":
    main()