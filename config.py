import threading
import multiprocessing

# Configs
multi_tasking = "multi_processing" # or "multi_processing"

processing_unit = None
if multi_tasking == "multi_threading":
    processing_unit = threading.Thread
elif multi_tasking == "multi_processing":
    processing_unit = multiprocessing.Process
