# cloud
Desenvolvimento para analises em cloud

## aws-py-ec2-describe.py

A ideia desse script é fazer uma varredura no EC2 em todas as regiões e retornar um csv contendo:
- Conta;
- Região;
- Id da instancia;
- Tipo da instancia;
- Lifecycle (se é spot, ondemand ou reserved);
- Platform (windows/linux/unix);
- Tag Name;
- Estado da instancia

Para utilizar o script:

python3 aws-py-ec2-describe.py -p <[profile]>
  
exemplo:
```
root@learntofly:/mnt/c/thiagosagaracloud# python3 aws-py-ec2-describe.py -p SAGARA
account,region,instanceid,instancetype,hostname,state
SAGARA,sa-east-1,i-041f3bd11e590591a,t3a.small,Carlos Adao,running
SAGARA,us-east-1,i-0ee8dd6ba1d497c53,t3a.small,Sem Hostname,running
```

