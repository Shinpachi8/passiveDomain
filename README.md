# passiveDomain

这是一个被动域名收集的脚本，不进行DNS爆破，只通过不同渠道的DNS集合来收集测试所需要的域名
## 使用步骤

- 使用之前请先按照[DNSGrep](https://github.com/erbbysam/DNSGrep) 中 [fdns_a](https://github.com/erbbysam/DNSGrep/blob/master/scripts/fdns_a.sh)的脚本将最新的opendata下载更新并排
- 在reverse_search中将FPATH 修改为对应的文件路径
- `python fetchfld.py domain.com domain_out.txt ip_out.txt`

## 包含数据
目前的途径包括:
    - rapid7 opendata fdns_a.tar.gz
    - ip138
    - crt.sh
自己可以添加wydomain中使用到的 chaxunla, googlect, ilnks, passivetotal 等接口来查询

## 工作流程
主要的流程:
    - 利用DNSGrep的脚本将其做排序处理, 以便快速的查询
    - 利用crt.sh获取域名下的所有证书中保存的主域名, 然后利用上一次的结果找查
    - 利用ip138的接口来查询不同主域名下的子域名

## TODO
尚未完成的工作:
    - 识别CDN的域名
    - 识别CDN的IP
