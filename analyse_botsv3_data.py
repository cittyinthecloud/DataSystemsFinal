#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv("botsv3_stream.csv")

df = df[~df["flow_id"].isnull()] # Filter out flows without IDs (incorrect parsing?)

df["bytes_total"] = df["bytes_in"] + df["bytes_out"]


    
plt.title("Length in bytes of ICMP flows")
plt.hist(df[df["protocol"]=="icmp"]["bytes_total"],bins=30)
plt.show()

plt.title("Length in bytes of TCP flows")
plt.hist(df[df["protocol"]=="tcp"]["bytes_total"],bins=30, range=(0,256000))
plt.show()

plt.title("Length in bytes of UDP flows")
plt.hist(df[df["protocol"]=="udp"]["bytes_total"],bins=30, range=(0,2048))
plt.show()