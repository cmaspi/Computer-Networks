sudo tc qdisc add dev h2-eth0 root netem rate 10Mbit limit 100 delay 5ms loss 5%