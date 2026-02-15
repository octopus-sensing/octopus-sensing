import os.path
import time
from typing import List

def wait_until_path_exists(paths: List[str], timeout: int = 5) -> bool:
    '''Wait until all the paths exist, with a timeout.

    Parameters
    ----------
    paths: List[str]
        List of paths (file, directory, etc.) to check for existence.
    timeout: int
        Maximum time to wait in seconds.

    Returns
    -------
    bool
        True if all paths exist within the timeout, False otherwise.

    '''
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        if all(os.path.exists(path) for path in paths):
            return True
        time.sleep(0.1)
    return False

def wait_until_file_updated(file_path: str, previous_size: int, timeout: int = 5) -> bool:
    '''Wait until the file exists and is updated (size changes), with a timeout.

    Parameters
    ----------
    file_path: str
        Path to the file to check for updates.
    previous_size: int
        The previous size of the file in bytes.
    timeout: int
        Maximum time to wait in seconds.

    Returns
    -------
    bool
        True if the file is updated within the timeout, False otherwise.

    '''
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        if os.path.exists(file_path) and os.path.getsize(file_path) > previous_size:
            return True
        time.sleep(0.1)
    return False
