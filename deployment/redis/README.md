# Redis
Currently we use the bitnami redis chart from https://artifacthub.io/packages/helm/bitnami/redis

From within the cluster you can access the redis instance at redis://redis-master.redis.svc.cluster.local:6379.
See also the settings.py file in the django folder.

## Debugging
For debugging purposes you can enter the redis pod as usual and run `redis-cli`.
If you want to check if the django wrote the cache you have to
```bash
# select the db django is using (see settings.py)
SELECT 1 
KEYS *
```