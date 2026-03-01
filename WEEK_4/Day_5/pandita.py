import pandas as pd

df = pd.read_csv(r"C:\Users\pbiai\Desktop\IRONHACK-BOOTCAMP\WEEK_4\Day_5\data.csv")
qualified = df[df["score"] == "Qualified"]
print(qualified)