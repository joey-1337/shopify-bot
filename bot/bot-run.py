#! /usr/bin/python
try:
    from bot import master
except ImportError: 
    import master

while True:
    master.bot()
