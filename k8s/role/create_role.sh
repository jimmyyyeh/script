# sh ./create.sh $1=使用者名稱 $2=namespace $3=echo "APISERVER=$(kubectl config view --minify | grep server | cut -f 2- -d ":" | tr -d " ")"

openssl genrsa -out $1.key 2048 
openssl req -new -key $1.key -out $1.csr -subj "/CN=$1"

cat <<EOF | kubectl create -f -
apiVersion: certificates.k8s.io/v1beta1
kind: CertificateSigningRequest
metadata:
  name: $1-csr
spec:
  groups:
  - system:authenticated
  request: $(cat $1.csr | base64 | tr -d '\n')
  usages:
  - digital signature
  - key encipherment
  - client auth
EOF

kubectl certificate approve $1-csr

kubectl get csr $1-csr -o jsonpath='{.status.certificate}' | base64 -D > $1.crt

kubectl create rolebinding $1 \
--clusterrole=read-pods --user=$1 --namespace=$2

kubectl config set-cluster $1-cluster \
  --insecure-skip-tls-verify=true \
  --server=$3 \
  --kubeconfig=$1.kubeconfig
kubectl config set-credentials $1 \
  --client-certificate=$1.crt \
  --client-key=$1.key \
  --embed-certs=true \
  --kubeconfig=$1.kubeconfig
kubectl config set-context $1 \
  --cluster=$1-cluster \
  --user=$1 \
  --namespace=$2 \
  --kubeconfig=$1.kubeconfig
