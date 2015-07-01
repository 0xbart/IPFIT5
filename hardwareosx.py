import os

# List hardware on OSx

os.system("system_profiler | grep 'Serial Number (system)' | grep 'Hardware UUID" | grep 'kind')
