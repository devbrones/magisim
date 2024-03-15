from zlib import crc32
import pickle


class Project:
    # the project class defines the general data structure of a magisim project.
    # it will contain the following:
    # - name: the name of the project
    # - extensions: a list of all loaded extensions
    # - node-json: a json object of the raw data from the node system, which will be uploaded to the node manager (how the fuck)
    # - 







class mse:
    @staticmethod
    def read(path: str):
        """
        The `read` function reads a file with a specific format, verifies the header and checksum, and
        returns a SimpleObject with the name and data from the file.
        
        :param path: The `path` parameter is a string that represents the file path of the file you want
        to read. It should be the absolute or relative path to the file you want to open and read
        :type path: str
        :return: a SimpleObject, which is created using the name and data read from the file.
        """
        # open the file
        with open(path, 'rb') as f:
            # read the header (first 72 bytes)
            header = f.read(72)
            # | magic number | version | name     | compression type | compressed size | uncompressed size | checksum |
            # |--------------|---------|----------|------------------|-----------------|-------------------|----------|
            # | 4 bytes      | 4 bytes | 32 bytes | 12 bytes         | 4 bytes         | 4 bytes           | 12 bytes |
            # | "MSEF"       | "1"     | name     | "none"           | 0               | 0                 | CRC32    |
            # check the magic number
            if header[:4] != b'MSEF':
                raise ValueError('Invalid magic number')
            # check the version
            if header[4:8].rstrip(b'\x00') != b'1':
                raise ValueError('Invalid version')
            # read the name
            name = header[8:40].decode('utf-16le').rstrip('\x00')
            # read the compression type
            compression = header[40:52].decode('utf-16le').rstrip('\x00')
            # read the compressed size
            compressed = int.from_bytes(header[52:56], 'little')
            # read the uncompressed size
            uncompressed = int.from_bytes(header[56:60], 'little')
            # read the checksum
            checksum = int.from_bytes(header[60:72], 'little')
            # read the data (excluding the header)
            f.seek(72, 0)
            rawdata = f.read()
            data = pickle.loads(rawdata)
            # check the checksum
            if crc32(rawdata) != checksum:
                raise ValueError('Invalid checksum')
            # create a simple object object
            return data
        
    @staticmethod
    def save(obj: Project, path: str):
        """
        The function saves a Project to a file by writing its header and data.
        
        :param obj: The `obj` parameter is an instance of the `Project` class. It represents an
        object that you want to save to a file
        :type obj: Project
        :param path: The `path` parameter is a string that represents the file path where the project
        will be saved. It should include the file name and extension.
        :type path: str
        """
        with open(path, 'wb') as f:
            header = b'MSEF' + b'1'.ljust(4, b'\x00') + obj.name.encode('utf-16le').ljust(32, b'\x00') + b'none'.ljust(12, b'\x00')
            header += (0).to_bytes(4, 'little') + (0).to_bytes(4, 'little')
            header += crc32(pickle.dumps(obj.data)).to_bytes(12, 'little')
            f.write(header)
            f.write(pickle.dumps(obj.data))
        
        return path




