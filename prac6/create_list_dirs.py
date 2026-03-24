import os

os.makedirs("parent/child/grandchild", exist_ok=True)
print("Contents :")
print(os.listdir("parent"))