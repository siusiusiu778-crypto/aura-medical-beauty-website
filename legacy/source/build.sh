#!/bin/sh
cd /home/claude/pages && python3 svc.py >/dev/null && python3 mem.py >/dev/null && python3 col.py && python3 build_home.py
