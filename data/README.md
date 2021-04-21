# Usage

```bash
#log.sh
../log.sh [name]


# cov_script
../../result/cov_script_showmap_live555.sh ../../result/results-live555-3600/out-live555-aflnet-1 8554 5 1
```

# lightftp

```
python $FUZZSCRIPT/bench_edge_store.py -s 3600 -d lightftp -p FTP
```

```bash
# prepare
cd /home/ubuntu/experiments/LightFTP/Source/Release

# run
mkdir lightftp/3600/out-lightftp-aflnet/trace_data
cov_script_showmap_lightftp lightftp/3600/out-lightftp-aflnet 2200 5 1

mkdir lightftp/3600/out-lightftp-aflnwe/trace_data
cov_script_showmap_lightftp lightftp/3600/out-lightftp-aflnwe 2200 5 0

mkdir lightftp/3600/out-lightftp-afldev/trace_data
cov_script_showmap_lightftp lightftp/3600/out-lightftp-afldev 2200 5 1


cd lightftp/86400/
l
cd ../../
mkdir lightftp/86400/out-lightftp-aflnet/trace_data
cov_script_showmap_lightftp lightftp/86400/out-lightftp-aflnet 2200 5 1

mkdir lightftp/86400/out-lightftp-aflnwe/trace_data
cov_script_showmap_lightftp lightftp/86400/out-lightftp-aflnwe 2200 5 0

mkdir lightftp/86400/out-lightftp-afldev/trace_data
cov_script_showmap_lightftp lightftp/86400/out-lightftp-afldev 2200 5 1



tar -zcvf out-lightftp-aflnet.tar.gz out-lightftp-aflnet
tar -zcvf out-lightftp-afldev.tar.gz out-lightftp-afldev
tar -zcvf out-lightftp-aflnwe.tar.gz out-lightftp-aflnwe

tar -zxvf out-lightftp-afldev.tar.gz
tar -zxvf out-lightftp-aflnet.tar.gz
tar -zxvf out-lightftp-aflnwe.tar.gz
```
