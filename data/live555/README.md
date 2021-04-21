# Usage

```bash
#log.sh
../log.sh [name]


# cov_script
../../result/cov_script_showmap_live555.sh ../../result/results-live555-3600/out-live555-aflnet-1 8554 5 1
```

# live555

```
python $FUZZSCRIPT/bench_edge_store.py -s 3600 -d live555 -p FTP
```

```bash
# prepare
cd /home/ubuntu/experiments/live555/testProgs

# run
cov_script_showmap_live555 live555/3600/out-live555-aflnet 2200 5 1
cov_script_showmap_live555 live555/3600/out-live555-aflnwe 2200 5 0
cov_script_showmap_live555 live555/3600/out-live555-afldev 2200 5 1


cov_script_showmap_live555 live555/86400/out-live555-aflnet 2200 5 1
cov_script_showmap_live555 live555/86400/out-live555-aflnwe 2200 5 0
cov_script_showmap_live555 live555/86400/out-live555-afldev 2200 5 1


cov_script_showmap_live555 live555/18000/out-live555-aflnet 2200 5 1
cov_script_showmap_live555 live555/18000/out-live555-afldev 2200 5 1

cov_script_showmap_live555 live555/18000/out-live555-aflnwe 2200 5 0



tar -zcvf out-live555-aflnet.tar.gz out-live555-aflnet
tar -zcvf out-live555-afldev.tar.gz out-live555-afldev
tar -zcvf out-live555-aflnwe.tar.gz out-live555-aflnwe

tar -zxvf out-live555-afldev.tar.gz > /dev/null
tar -zxvf out-live555-aflnet.tar.gz > /dev/null
tar -zxvf out-live555-aflnwe.tar.gz > /dev/null
```
