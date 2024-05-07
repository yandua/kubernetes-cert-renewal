import subprocess
import csv


class RenewClusterCertificates():
    def __init__(self):
        pass
    
    def renew_certs():
        # renew CA cert and key
        cfssl = subprocess.Popen(("cfssl", "gencert", "-initca", "ca-csr.json"), stdout=subprocess.PIPE)
        output = subprocess.check_output(("cfssljson", "-bare", "ca"), stdin=cfssl.stdout)
        cfssl.wait()

        # renew admin certificate
        cfssl = subprocess.Popen(("cfssl", "gencert", "-ca=ca.pem", "-ca-key=ca-key.pem", "-config=ca-config.json", "-profile=kubernetes", "admin-csr.json"), stdout=subprocess.PIPE)
        output = subprocess.check_output(("cfssljson", "-bare", "admin"), stdin=cfssl.stdout)
        cfssl.wait()
        
        # generate controller manager cert
        cfssl = subprocess.Popen(("cfssl", "gencert", "-ca=ca.pem", "-ca-key=ca-key.pem", "-config=ca-config.json", "-profile=kubernetes", "kube-controller-manager-csr.json"), stdout=subprocess.PIPE)
        output = subprocess.check_output(("cfssljson", "-bare", "kube-controller-manager"), stdin=cfssl.stdout)
        cfssl.wait()
        
        # generate kube-proxy cert
        cfssl = subprocess.Popen(("cfssl", "gencert", "-ca=ca.pem", "-ca-key=ca-key.pem", "-config=ca-config.json", "-profile=kubernetes", "kube-proxy-csr.json"), stdout=subprocess.PIPE)
        output = subprocess.check_output(("cfssljson", "-bare", "kube-proxy"), stdin=cfssl.stdout)
        cfssl.wait()
        
        # generate kube-scheduler certificate
        cfssl = subprocess.Popen(("cfssl", "gencert", "-ca=ca.pem", "-ca-key=ca-key.pem", "-config=ca-config.json", "-profile=kubernetes", "kube-scheduler-csr.json"), stdout=subprocess.PIPE)
        output = subprocess.check_output(("cfssljson", "-bare", "kube-scheduler"), stdin=cfssl.stdout)
        cfssl.wait()
       
        # generate Service Account cert
        cfssl = subprocess.Popen(("cfssl", "gencert", "-ca=ca.pem", "-ca-key=ca-key.pem", "-config=ca-config.json", "-profile=kubernetes", "service-account-csr.json"), stdout=subprocess.PIPE)
        output = subprocess.check_output(("cfssljson", "-bare", "service-account"), stdin=cfssl.stdout)
        cfssl.wait()
        
        # generate machine certificates
        with open("clusterinfo.csv", newline="") as csvfile:
            clusterinfo = csv.reader(csvfile)
            next(clusterinfo, None)  # skip the headers
            for row in clusterinfo:
                if row[0] == "hostnames":
                    KUBERNETES_HOSTNAMES = row[2]
                if row[0] == "addresses":
                    KUBERNETES_IPS = row[2]
                if row[0] == "worker":
                  cfssl = subprocess.Popen(("cfssl", "gencert", "-ca=ca.pem", "-ca-key=ca-key.pem", "-config=ca-config.json", f"-hostname={row[1]},{row[2]}", "-profile=kubernetes",f"{row[1]}-csr.json"), stdout=subprocess.PIPE)
                  output = subprocess.check_output(("cfssljson", "-bare", row[1]), stdin=cfssl.stdout)
                  cfssl.wait()
                else: pass
     
        cfssl = subprocess.Popen(("cfssl", "gencert", "-ca=ca.pem", "-ca-key=ca-key.pem", "-config=ca-config.json", f"-hostname={KUBERNETES_IPS},{KUBERNETES_HOSTNAMES}", "-profile=kubernetes", "kubernetes-csr.json"), stdout=subprocess.PIPE)
        output = subprocess.check_output(("cfssljson", "-bare", "kubernetes"), stdin=cfssl.stdout)
        cfssl.wait()
        

if __name__ == "__main__":
    renewal = RenewClusterCertificates.renew_certs()
    print("Done!")







