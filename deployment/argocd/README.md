# ArgoCD
Currently argocd is just deployed by running kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
The problem is that this yaml always changes. We should probably deploy it via community supported helm chart: https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd

## Setup the CLI
https://argo-cd.readthedocs.io/en/stable/cli_installation/

## Adding Users

For the image update we need a local user. We can just modify the argocd-cm configmap according to https://argo-cd.readthedocs.io/en/stable/operator-manual/user-management/
