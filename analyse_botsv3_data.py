#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Caleb Gindelberger, Ricky Yoder
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("botsv3_stream.csv")

df = df[~df["flow_id"].isnull()] # Filter out flows without IDs (incorrect parsing?)

df["bytes_total"] = df["bytes_in"] + df["bytes_out"]

df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index("timestamp" ,inplace=True)

#Visualizations    
plt.title("Length in bytes of ICMP flows")
plt.hist(df[df["protocol"]=="icmp"]["bytes_total"],bins=30)
plt.show()

plt.title("Length in bytes of TCP flows")
plt.hist(df[df["protocol"]=="tcp"]["bytes_total"],bins=30, range=(0,256000))
plt.show()

plt.title("Length in bytes of UDP flows")
plt.hist(df[df["protocol"]=="udp"]["bytes_total"],bins=30, range=(0,2048))
plt.show()

plt.title("Percentage of Each Type of Protocol")
plt.pie(df["protocol"].value_counts(), labels = df["protocol"].value_counts().index,
        autopct='%1.1f%%')
plt.show()

plt.title("Total Bytes Over Time")
plt.plot(df.index.sort_values(),df["bytes_total"].sort_index().cumsum())
plt.xticks(rotation=45)
plt.show()

#Queries
#Most Active dest_ip (Total requests)
print(df["dest_ip"].value_counts().sort_values(ascending=False).index[0])

#Dest_ip with most bytes sent to it 
grpbyDest = df.groupby("dest_ip")
print(grpbyDest.agg({"bytes_out":"sum"})
      .sort_values(by= "bytes_out",ascending=False).index[0])

#Dest_ip that spent the most time
print(grpbyDest.agg({"time_taken":"sum"})
      .sort_values(by= "time_taken",ascending=False).index[0]) #Most time = most bytes
