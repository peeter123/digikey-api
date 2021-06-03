#!/usr/bin/python3

# Query a fresh user agent
from fake_useragent import UserAgent

print('<'+UserAgent().firefox+'>')
