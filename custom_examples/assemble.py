import subprocess
import sys
import os

file_path = os.path.abspath(sys.argv[1])

if not os.path.isfile(file_path):
    raise Exception("File does not exist %s" % file_path)

out_file = os.path.splitext(file_path)[0] + ".md"

p = subprocess.Popen(["vasmm68k_std",
                      "-o", out_file,
                      "-quiet",
                      "-Fbin",
                      file_path])
p.communicate()
if p.poll() != 0:
    print("error")
else:
    print("Wrote " + out_file)
