# KubeFlow-Sample


# 🚀 Kubeflow Pipelines Setup on Minikube

This guide provides step-by-step instructions to **install Kubeflow Pipelines (KFP) on Minikube**, build pipelines, and run them successfully.

---

# 📌 Prerequisites

* Docker installed
* Minikube installed
* kubectl installed
* Python 3.9+

---

# ⚙️ Step 1: Start Minikube

```bash
minikube start --cpus=4 --memory=8192 --driver=docker --force

```

Verify cluster:

```bash
kubectl get nodes
```

---

# ⚙️ Step 2: Install Kubeflow Pipelines

Install latest KFP manifests:

```bash
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=master"
kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=master"
```

---

# ⚙️ Step 3: Verify Installation

```bash
kubectl get pods -n kubeflow
```

✅ Ensure all pods are:

```
Running (1/1)
```

---

# ⚙️ Step 4: Access KFP UI

```bash
kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
```

Open:

```
http://localhost:8080
```

---

# ⚙️ Step 5: Setup Python Environment

```bash
pip install kfp==2.9.0
```

---

# ⚙️ Step 6: Create Pipelines

## Example: Hello Pipeline

```python
from kfp import dsl, compiler

@dsl.component(base_image="python:3.9-slim")
def say_hello(name: str) -> str:
    print(f"Hello, {name}!")
    return f"Hello, {name}!"

@dsl.pipeline(name="hello-world-pipeline")
def hello_pipeline(recipient: str = "World"):
    say_hello(name=recipient)

if __name__ == "__main__":
    compiler.Compiler().compile(
        hello_pipeline,
        "hello_world_pipeline.yaml"
    )
```

---

## Example: Iris ML Pipeline

```python
import kfp
from kfp import dsl
from typing import NamedTuple, List

@dsl.component(base_image="python:3.9-slim", packages_to_install=["pandas","scikit-learn"])
def load_data() -> NamedTuple("Outputs",[("features",List[List[float]]),("labels",List[int])]):
    from sklearn.datasets import load_iris
    iris = load_iris()
    return (iris.data.tolist(), iris.target.tolist())

@dsl.component(base_image="python:3.9-slim", packages_to_install=["scikit-learn"])
def train_model(features: List[List[float]], labels: List[int]) -> NamedTuple("Output",[("accuracy",float)]):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    acc = accuracy_score(y_test, clf.predict(X_test))
    print(f"Accuracy: {acc}")
    return (acc,)

@dsl.pipeline(name="iris-pipeline")
def iris_pipeline():
    data = load_data()
    train_model(features=data.outputs["features"], labels=data.outputs["labels"])

if __name__ == "__main__":
    kfp.compiler.Compiler().compile(iris_pipeline, "iris_pipeline.yaml")
```

---

# ⚙️ Step 7: Compile Pipelines

```bash
python3 hello_pipeline.py
python3 iris_pipeline.py
```

---

# ⚙️ Step 8: Upload Pipeline (Python SDK)

Create file `test.py`:

```python
from kfp import Client

client = Client(host="http://localhost:8080/pipeline")

client.upload_pipeline(
    pipeline_package_path="iris_pipeline.yaml",
    pipeline_name="iris_pipeline"
)
```

Run:

```bash
python3 test.py
```

---

# ⚙️ Step 9: Run Pipeline

1. Open UI → http://localhost:8080
2. Go to **Pipelines**
3. Select pipeline
4. Click **Create Run** → Start

---

# 🔍 Verification

Check logs:

```bash
kubectl get pods -n kubeflow
kubectl logs <pod-name> -n kubeflow
```

Expected output:

```
Model accuracy: 0.9+
```

---

# ⚠️ Troubleshooting

## ImagePullBackOff

* Use latest manifests (`ref=master`)
* Avoid deprecated images

## UI slow / stuck

```bash
kubectl port-forward restart
```

## Check pod logs

```bash
kubectl describe pod <pod-name> -n kubeflow
```

---

# 🎯 Summary

* Minikube cluster setup ✅
* Kubeflow Pipelines installed ✅
* Pipelines compiled & uploaded ✅
* ML pipeline executed successfully ✅

---

Screenshots : 
<img width="1853" height="1011" alt="image" src="https://github.com/user-attachments/assets/3c729efa-93fa-407c-9a3a-1b5b98a2eda6" />
<img width="1843" height="1080" alt="image" src="https://github.com/user-attachments/assets/8c0a72bc-47fe-4c5f-8dd4-760d4b12bb4c" />
<img width="1843" height="1080" alt="image" src="https://github.com/user-attachments/assets/f6cc96af-3488-4785-953b-70fe0e8952dd" />
<img width="1835" height="1080" alt="image" src="https://github.com/user-attachments/assets/4c2fabd1-1dc2-4065-8709-e92dcf797859" />
<img width="1835" height="1080" alt="image" src="https://github.com/user-attachments/assets/b38309a2-de6e-46cc-bacb-e692332e0d0b" />



