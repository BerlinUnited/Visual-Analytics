# ArgoCD
Currently argocd is just deployed by running kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
The problem is that this yaml always changes. We should probably deploy it via community supported helm chart: https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd

## Setup ArgoCD
Create namespace
```bash
kubectl create namespace argocd
```

Install the helm chart
```bash
helm upgrade --install -f values.yaml argocd . --namespace argocd
```

Currently the base application is still handled by click ops. Important to note there is that the 
- project default
- namespace: argocd, 
- cluster: https://kubernetes.default.svc
- repo: git@github.com:efcy/visual_analytics.git
- path: deployment/base

## Setup the CLI
https://argo-cd.readthedocs.io/en/stable/cli_installation/



## Adding Users
For the image updater we need a user which can have an api key. But this is not possible for the admin user.
You can add a user in the values.yaml. This user will have the admin role by default.

After adding the user you need the cli to change the password
```bash
 argocd account update-password --account <account name>
```
If you need an api token you can create that in the UI or with the Argocd CLI

To have argocd reflect the new user you need to restart the argocd-server:
```bash
kubectl rollout restart deployment argocd-server -n argocd
```

## Image Updater
https://argocd-image-updater.readthedocs.io/en/stable/install/installation/ 