#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Caleb Gindelberger, Ricky Yoder
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import pygraphviz_layout

df = pd.read_csv("botsv3_stream.csv")

df.dtypes
df.shape
df.describe()
df.columns
    
df = df[~df["flow_id"].isnull()] # Filter out flows without IDs (incorrect parsing?)

df["bytes_total"] = df["bytes_in"] + df["bytes_out"]

df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index("timestamp" ,inplace=True)

#Visualizations
# Graph 1
plt.title("Length in bytes of ICMP flows")
plt.hist(df[df["protocol"]=="icmp"]["bytes_total"],bins=30)
plt.show()

# Graph 2
plt.title("Length in bytes of TCP flows")
plt.hist(df[df["protocol"]=="tcp"]["bytes_total"],bins=30, range=(0,256000))
plt.show()

# Graph 3
plt.title("Length in bytes of UDP flows")
plt.hist(df[df["protocol"]=="udp"]["bytes_total"],bins=30, range=(0,2048))
plt.show()

# Graph 4

plt.title("Percentage of Each Type of Protocol")
plt.pie(df["protocol"].value_counts(), labels = df["protocol"].value_counts().index,
        autopct='%1.1f%%')
plt.show()

# Graph 5 

plt.title("Total Bytes Over Time")
plt.plot(df.index.sort_values(),df["bytes_total"].sort_index().cumsum())
plt.xticks(rotation=45)
plt.show()

# Graph 6
counts = df.groupby(["src_ip","dest_ip"]).size().reset_index(name="counts")

connections = set(tuple(x) for x  in counts[counts["counts"] > 100][["src_ip","dest_ip"]].to_numpy())

all_ips = set(ip for conn in connections for ip in conn)

g = nx.DiGraph()

g.add_nodes_from(all_ips)

for conn in connections:
    g.add_edge(*conn)
    
plt.figure(figsize=(16, 12), dpi=80)
nx.draw_networkx(g, pos=pygraphviz_layout(g, prog="fdp"))


#Queries
#top 3 Most Active dest_ip (Total flows) *Written With*
print(df["dest_ip"].value_counts().sort_values(ascending=False).index[0:3]) 

#Top 3 Dest_ips with most bytes sent to it  *Written with*
grpbyDest = df.groupby("dest_ip")
print(grpbyDest.agg({"bytes_out":"sum"})
      .sort_values(by= "bytes_out",ascending=False).index[0:3])

#top 3 Dest_ips that spent the most time *Written With*
print(grpbyDest.agg({"time_taken":"sum"})
      .sort_values(by= "time_taken",ascending=False).index[0:3]) #Most time = most bytes but not all 3

#Top 3 apps that were used the most
print(df["app"].value_counts().sort_values(ascending=False).index[0:3])

#Which protocol was used to move the most bytes_total *Written with*
grpbyProt = df.groupby("protocol")
print(grpbyProt.agg({"bytes_total":"sum"})
      .sort_values(by= "bytes_total",ascending=False).index[0]) #tcp, even though udp was used the most which makes sense bc tcp is used for file transfer

#top 3 protocols by time taken *written with*
print(grpbyProt.agg({"time_taken":"sum"})
      .sort_values(by= "time_taken",ascending=False).index[0:3])

#which protocol had the most unique apps 
print(grpbyProt.agg({"app": pd.Series.nunique})
      .sort_values(by = "app", ascending=False).index[0:3]) #tcp surprising given how many more udp usages there are

#amount of unhashed flows *Written with*
print(grpbyProt.agg({"src_content_hash": lambda x: sum(x.isna())})
      .sort_values(by = "src_content_hash", ascending=False).index[0:3]) #tcp had the highest amount of unhashed flows

print(df["protocol"].value_counts())

#Top 3 src_ips with the most unique dest_ips *written with*
print(df.groupby("src_ip").agg({"dest_ip": pd.Series.nunique})
      .sort_values(by = "dest_ip", ascending=False).index[0:3])


# Correlation between bytes and time taken
print(df[["time_taken","bytes_in","bytes_out","bytes_total"]].corr())
