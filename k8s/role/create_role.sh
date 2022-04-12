# sh ./create.sh $1=使用者名稱 $2=cluster name $3=role $4=namespace $api_server
# APISERVER=$(kubectl config view --minify | grep server | cut -f 2- -d ":" | tr -d " ")

USERNAME=$1
CLUSTER_NAME=$2
ROLE=$3
NAMESPACE=$4
APISERVER=$5
KUBE_CONFIG=$USERNAME.kubeconfig
KEY=$USERNAME.key
CRT=$USERNAME.crt
CSR=$USERNAME.csr

## *** 如果下列檔案都產好了 可以只執行這一行就好 單純建立角色***
kubectl create rolebinding $USERNAME \
--clusterrole=$ROLE --user=$USERNAME --namespace=$NAMESPACE

# 產生.key file
if ! test -f "$KEY"; then
    echo "========== GENERATE NEW $KEY =========="
    openssl genrsa -out $USERNAME.key 2048
fi

# 產生.csr file
if ! test -f "$CSR"; then
    echo "========== GENERATE NEW $CSR =========="
    openssl req -new -key $USERNAME.key -out $USERNAME.csr -subj "/CN=$USERNAME"
fi

cat <<EOF | kubectl create -f -
apiVersion: certificates.k8s.io/v1beta1
kind: CertificateSigningRequest
metadata:
  name: $USERNAME-csr
spec:
  groups:
  - system:authenticated
  request: $(cat $USERNAME.csr | base64 | tr -d '\n')
  usages:
  - digital signature
  - key encipherment
  - client auth
EOF

kubectl certificate approve $USERNAME-csr

# 產生.crt file
if ! test -f "$CRT"; then
    echo "========== GENERATE NEW $CRT =========="
    kubectl get csr $USERNAME-csr -o jsonpath='{.status.certificate}' | base64 -D > $USERNAME.crt
fi

# 產生kubeconfig file
if ! test -f "$KUBE_CONFIG"; then
    echo "========== GENERATE NEW $KUBE_CONFIG =========="
    kubectl config set-cluster $CLUSTER_NAME-cluster \
      --insecure-skip-tls-verify=true \
      --server=$APISERVER \
      --kubeconfig=$USERNAME.kubeconfig
fi

# 建立user
kubectl config set-credentials $USERNAME \
  --client-certificate=$USERNAME.crt \
  --client-key=$USERNAME.key \
  --embed-certs=true \
  --kubeconfig=$USERNAME.kubeconfig
# 建立context
kubectl config set-context $CLUSTER_NAME-cluster \
  --cluster=$CLUSTER_NAME-cluster \
  --user=$USERNAME \
  --namespace=$NAMESPACE \
  --kubeconfig=$USERNAME.kubeconfig

kubectl config use-context $CLUSTER_NAME-cluster

# ***多個namespace的話最後再執行這行***
# 備份原本config檔案 避免遺失
mv ~/.kube/config ~/.kube/config.bak
# 覆蓋config檔案
cp $USERNAME.kubeconfig ~/.kube/config