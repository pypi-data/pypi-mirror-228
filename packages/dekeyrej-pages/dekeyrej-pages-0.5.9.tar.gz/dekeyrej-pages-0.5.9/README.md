# pages latest {version='0.5.9'}
Matrix - serverpage and displaypage classes

Incorporates dekeyrej-kube to interact with Kubernetes Secrets and ConfigMaps


**Pages have been split (in __init__.py)**

now requires:
- from pages.displaypage import DisplayPage
- from pages.serverpage import ServerPage

*securedict has been relegated to 'other method'*
- reads encoded secrets from inside kubernetes cluster, or
- reads from JSON file