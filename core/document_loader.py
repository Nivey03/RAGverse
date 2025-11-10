import os
from typing import List, Dict

class DocumentLoader:
    def __init__(self, data_dir: str):
        """
        Initialize the document loader

        Args:
            data_dir (str): Path to directory containing documents
        """
        self.data_dir = data_dir

    def load_documents(self) -> List[Dict[str, str]]:
        """
        Load all .txt files from the data directory

        Returns:
            List[Dict]: List of documents with 'content' and 'source' keys
            Example: [
                {'content': 'Document text...', 'source': 'file1.txt'},
                {'content': 'More text...', 'source': 'file2.txt'}
            ]
        """
        documents = []

        if not os.path.exists(self.data_dir):
            print(f"Warning: Directory {self.data_dir} does not exist!")
            return documents

        for filename in os.listdir(self.data_dir):
            if filename.endswith('.txt'):
                filepath = os.path.join(self.data_dir, filename)

                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    documents.append({
                        'content': content,
                        'source': filename
                    })
                    print(f"Loaded: {filename}")

                except Exception as e:
                    print(f"Error loading {filename}: {e}")

        print(f"\nTotal documents loaded: {len(documents)}")
        return documents