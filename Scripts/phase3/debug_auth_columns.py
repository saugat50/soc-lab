import pandas as pd

normal = pd.read_json("data/raw/auth/auth_normal.json", lines=True)
attack = pd.read_json("data/raw/auth/auth_attacks.json", lines=True)

print("NORMAL columns:")
print(normal.columns.tolist())

print("\nATTACK columns:")
print(attack.columns.tolist())

print("\nSample normal row:")
print(normal.head(1).to_dict())

print("\nSample attack row:")
print(attack.head(1).to_dict())
