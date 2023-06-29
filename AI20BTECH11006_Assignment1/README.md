I've added an interactive mode for client where the user could select the type of request, to run that pass the `-i` flag to the code in the console.

```
python3 client.py -i
```

The default behaviour is to first put all the (6) keys and retrieve each key either 3 or 4 times, 3 times for basic topology, 4 times for star topology.

The logs for client/cache/server can be found in respective log files which are overwritten in each run.
