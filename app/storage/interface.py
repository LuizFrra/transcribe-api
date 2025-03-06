from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO, Union

class StorageInterface(ABC):
    @abstractmethod
    def get(self, path: Union[str, Path]) -> BinaryIO:
        """
        Get a file from storage.
        
        Args:
            path (Union[str, Path]): Path to the file in storage
            
        Returns:
            BinaryIO: A file-like object containing the file data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            StorageError: If there's an error accessing storage
        """
        pass