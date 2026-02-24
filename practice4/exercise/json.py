import json
with open('sample-data.json') as data_file:
    data = json.load(data_file)

print("Interface Status")
print("="*80)
print(f"{'DN':50} {'Description':10} {'Speed':6} {'MTU':5}")
print("-" * 50, "-" * 10, "-" * 6, "-" * 5)
for i in range(len(data["imdata"])):
    a = data["imdata"][i]["l1PhysIf"]["attributes"]
    dn = a["dn"]
    descr = a["descr"]
    speed = a["speed"]
    mtu = a["mtu"]
    print(f"{dn:50} {descr:10} {speed:6} {mtu:5}")
