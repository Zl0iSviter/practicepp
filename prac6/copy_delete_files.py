import shutil
import os

# copy
shutil.copy("sample.txt", "sample_backup.txt")
print("File copied.")

# delete and backup
if os.path.exists("sample_backup.txt"):
    os.remove("sample_backup.txt")
    print("Backup deleted.")
else:
    print("Backup file not found.")