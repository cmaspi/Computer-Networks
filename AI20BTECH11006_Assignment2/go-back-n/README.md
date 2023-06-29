# How to RUN
```bash
sudo mn
```

Then in the mininet shell


```bash
xterm h1 & xterm h2
```

Kindly change the values in conditions shell files, and timeout, window size in `sender.py` to desired values.


In xTerm h2
```
fish conditions_receiver.fish
python3 AI20BTECH11006_receiverGBN.py
```

In xTerm h1
```
fish conditions_sender.fish
python3 AI20BTECH11006_senderGBN.py
```

You are good to go!
