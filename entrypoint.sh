#!/bin/sh

geth --datadir /root/data init /tmp/genesis.json
cp /tmp/keystore/* /root/data/keystore/

geth --networkid 66 \
    --datadir /root/data \
    --allow-insecure-unlock --password "/dev/null" --unlock 0 \
    --nodiscover --mine \
    --http \
    --http.corsdomain "*" --http.vhosts='*' \
    --http.addr=0.0.0.0 --http.port=8545 \
    --http.api web3,eth,debug,personal,net \
    --vmdebug \
    console \