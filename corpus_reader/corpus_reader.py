import datetime
import json
import mmap
import os
import unidecode

class CorpusReader:
    """_summary_
        A reader for efficiently accessing documents in a corpus using an index.
    """
    def __init__(self, index_path : str, verbose : bool = False):
        """_summary_
            Initialize the corpus reader using an pre-built index file.
        Args:
            index_path (str): Path of the pre-built index file.
            verbose (bool, optional): Whether to print the progress status or not. Defaults to False.
        """
        self.index = {}
        self.did_list = []
        self.data_offset = 0
        with open(f'{index_path}.idx', 'r', encoding='utf-8') as fp:
            for line in fp:
                self.data_offset += len(line)
                did, start_idx, end_idx = line.strip().split('\t')
                if (did, start_idx, end_idx) == ('0', '0', '0'):
                    break
                self.index[did] = {'start': int(start_idx), 'end': int(end_idx)}
                self.did_list.append(did)
        self.fp = open(f'{index_path}.idx', 'r+b')
        self.mm = mmap.mmap(self.fp.fileno(), 0)

    def __del__(self):
        """_summary_
            Clean up resources.
        """
        self.mm.close()
        self.fp.close()

    def __getitem__(self, index : int | str) -> str:
        """_summary_
            Fetch a document by its ID (str) or index (int).
        Args:
            index (int | str): The ID (str) or index (int) of the document.
        Returns:
            str: The fetched document.
        """
        did = self.did_list[index] if isinstance(index, int) else index
        doc = self.mm[self.data_offset+self.index[did]['start']:self.data_offset+self.index[did]['end']]
        doc = doc.decode()
        return doc

    def __len__(self) -> int:
        """_summary_
            Return the number of documents in the corpus.
        Returns:
            int: Number of documents in the corpus.
        """
        return len(self.did_list)

    @staticmethod
    def to_str(data):
        """_summary_
            Convert the given data into string representation.
        Args:
            data (str | list): Data to convert.
        Returns:
            str: String converted version of the given data.
        """
        if isinstance(data, str):
            return data
        if isinstance(data, list):
            return ' '.join([str(d) for d in data])
        return str(data)

    @staticmethod
    def build_index(data_path : str, index_path : str, keys : list[str], verbose : bool = False):
        """_summary_
            Build an index file for the given data file.
        Args:
            data_path (str): Path of the data file (json type).
            index_path (str): Path of the index file to be created.
            keys (list[str]): Keys of the data file to be indexed.
            verbose (bool, optional): Wheather to print the progress status or not. Defaults to False.
        """
        # Create index and data files
        with open(f'{index_path}.idx', 'w', encoding='utf-8') as fp_idx, open(f'{index_path}.data', 'w', encoding='utf-8') as fp_data, open(data_path, 'r', encoding='utf-8') as fp:
            file_name = data_path.split('/')[-1]
            cnt = 0
            cnt_doc = 0
            for line in fp:
                data = json.loads(line)
                did = data['id']
                doc = ' '.join([CorpusReader.to_str(data[key]) for key in keys]).strip()
                doc = unidecode.unidecode(doc)
                fp_data.write(doc)
                fp_idx.write(f'{did}\t{cnt}\t{cnt + len(doc)}\n')
                cnt += len(doc)
                cnt_doc += 1
                if verbose and cnt_doc % 10000 == 0:
                    now = datetime.datetime.now().strftime('%H:%M:%S')
                    print(f'[ {now} ] Corpus Reader | file: {file_name} | reading documents | doc: {cnt_doc:,} |', end='\r', flush=True)
            if verbose:
                now = datetime.datetime.now().strftime('%H:%M:%S')
                print(f'[ {now} ] Corpus Reader | file: {file_name} | reading documents | doc: {cnt_doc:,} |', flush=True)
            fp_idx.write('0\t0\t0\n')

        # Merge index and data files into one
        with open(f'{index_path}.idx', 'a', encoding='utf-8') as fp_idx, open(f'{index_path}.data', 'r', encoding='utf-8') as fp_data:
            for line in fp_data:
                fp_idx.write(line)
                if verbose and cnt_doc % 10000 == 0:
                    now = datetime.datetime.now().strftime('%H:%M:%S')
                    print(f'[ {now} ] Corpus Reader | file: {file_name} | merging index |', end='\r', flush=True)
            if verbose:
                now = datetime.datetime.now().strftime('%H:%M:%S')
                print(f'[ {now} ] Corpus Reader | file: {file_name} | merging index |', flush=True)
        os.remove(f'{index_path}.data')
