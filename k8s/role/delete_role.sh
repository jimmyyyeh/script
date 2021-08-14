kubectl config set-context --current --namespace=$2
kubectl delete csr $1-csr
kubectl delete rolebinding $1
