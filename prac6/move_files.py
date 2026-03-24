import shutil

shutil.move("sample.txt", "parent/sample_moved.txt")
shutil.copy("parent/sample_moved.txt", "sample_copy.txt")