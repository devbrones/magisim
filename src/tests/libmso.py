from zlib import crc32
import pickle

# The class SimpleObject represents an object with a name and data, and provides methods for string
# representation, equality comparison, and retrieving the shape of the data.
class SimpleObject:
    def __init__(self, name, data):
        """
        The above code defines a class called SimpleObject with various methods for string
        representation, equality comparison, and retrieving the shape of the data attribute.
        
        :param name: The `name` parameter is a string that represents the name of the object. It is used
        to identify the object and provide a human-readable representation of it
        :param data: The `data` parameter is a variable that represents some kind of data associated
        with the `SimpleObject` instance. It could be any type of data, such as a list, dictionary,
        string, or even a NumPy array. The specific type of data is not specified in the code snippet
        provided
        """
        self.name = name
        self.data = data
    def __repr__(self):
        return f'<SimpleObject name="{self.name}" data={self.data}>'
    def __str__(self):
        return f'SimpleObject(name="{self.name}", data={self.data})'
    def __eq__(self, other):
        return self.name == other.name and self.data == other.data
    def __ne__(self, other):
        return not self.__eq__(other)
    def get_shape(self):
        return self.data.shape

    


class mso:
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
            # | "MSOF"       | "1"     | name     | "none"           | 0               | 0                 | CRC32    |
            # check the magic number

            if header[:4] != b'MSOF':
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
            return SimpleObject(name, data)
        
    @staticmethod
    def save(obj: SimpleObject, path: str):
        """
        The function saves a SimpleObject to a file by writing its header and data.
        
        :param obj: The `obj` parameter is an instance of the `SimpleObject` class. It represents an
        object that you want to save to a file
        :type obj: SimpleObject
        :param path: The `path` parameter is a string that represents the file path where the object
        will be saved. It should include the file name and extension. For example, `path =
        "C:/data/object.bin"` would save the object to a file named "object.bin" in the "C:/data
        :type path: str
        """
        with open(path, 'wb') as f:
            header = b'MSOF' + b'1'.ljust(4, b'\x00') + obj.name.encode('utf-16le').ljust(32, b'\x00') + b'none'.ljust(12, b'\x00')
            header += (0).to_bytes(4, 'little') + (0).to_bytes(4, 'little')
            header += crc32(pickle.dumps(obj.data)).to_bytes(12, 'little')

            f.write(header)
            f.write(pickle.dumps(obj.data))
        
        return path




