sudo tc qdisc add dev h1-eth0 root netem rate 10Mbit limit 100 delay 5ms loss 5%
