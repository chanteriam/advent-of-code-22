
class File:
    """
    Provides implementation of a file class. Files are contained within
        directories.

    Attributes:
        name (str): name of the file
        size (int): size of the file
    """

    def __init__(self, size=0, name=""):
        """
        Initializes a file object.

        Inputs:
            name (str): name of the file
            size (int): size of the file
        """

        self.size = size
        self.name = name

    def __repr__(self):
        """
        Overrides default representation for printing a file object.

        Returns:
            (str) string representation of a file object
        """

        s = "File Name: {}\n".format(self.name)
        s += "File Size: {}".format(self.size)
        return s

    def __eq__(self, other):
        """
        Overrides default equality operator for a file object.

        Inputs:
            other (File): File object to compare self to

        Returns:
            (bool) True if file objects are equal, false otherwise
        """

        return (self.name == other.name)


class Directory:
    """
    Provides implementation of a directory class with a tree structure.
        Directories can contain other directories (tree) or files (leafs)

    Attributes:
        name (str): name of the directory
        size (int): size of the directory, equal to the sum of the size of
            all subdirectories and files
        subdirectories (lst): a list of directory objects within this directory
        files (lst): list of file objects (leaf nodes) within this directory
    """

    def __init__(self, name=""):
        """
        Initializes a directory object.

        Inputs:
            name (str): name of the directory
            size (int): size of the directory
        """

        self.name = name
        self.__size = 0
        self.subdirectories = []
        self.files = []

    def __repr__(self):
        """
        Overrides default representation for printing a directory object.

        Returns:
            (str) string representation of a directory object
        """
        return self.__to_string()

    def __to_string(self, tab_count=0):
        """
        Helper function to override default repr function. Provides string
            representation of a directory structure.

        Inputs:
            tab_count (int): indentation level of the current directory

        Returns:
            (string): string representation of the directory structure
        """

        s = "\t"*tab_count + \
            "- {} (dir, size = {}) \n".format(self.name, self.__size)

        for directory in self.subdirectories:
            s += directory.__to_string(tab_count+1)

        for file in self.files:
            f = "\t"*(tab_count+1) + \
                "- {} (file, size = {})\n".format(file.name, file.size)
            s += f

        return s

    def __eq__(self, other):
        """
        Overrides default equality operator for a directory object.

        Inputs:
            other (Directory): Directory object to compare self to

        Returns:
            (bool) True if directory objects are equal, false otherwise
        """

        return (self.name == other.name)

    def path_exists(self, path=""):
        """
        Determines if a path to a subdirectory or file exists.

        Inputs:
            path (str): path of subdirectory to find in directory structure

        Returns:
            (bool, str): tuple, true if path exists, false otherwise and type of
                object the path goes to (file or directory)
        """

        if (path == ""):  # base case
            return True, "directory"

        cur_dir = path[:path.index("/")]  # first sub-directory
        exists = cur_dir == self.name
        new_path = path[path.index("/")+1:]
        obj_type = "directory"  # file or directory

        # recursively determine if remainder of path exists
        if exists and len(new_path) > 0:

            # it's a subdirectory
            if "/" in new_path:
                for subdir in self.subdirectories:
                    exists, obj_type = subdir.path_exists(new_path)
                    if exists:
                        break

            # it's a file
            else:
                exists = File(0, new_path) in self.files
                obj_type = "file"

        return exists, obj_type

    def add_file(self, file, path=""):
        """
        Adds a file to a directory.

        Inputs:
            file (File): a file object to add to the directory's list of files
            path (str, optional): subdirectory to add file to; if not specified,
                file will be added to current directory

        Return:
            (str): message if file was successfully added
        """

        exists, obj_type = self.path_exists(path)

        if not exists:
            return "ERROR: Path doesn't exist"

        elif obj_type == "file":  # can't add a file to another file
            return "ERROR: cannot add a file to another file"

        else:
            message = ""
            if path == "":
                message = self.__add_subfile(file, path)

            # remove main
            else:
                message = self.__add_subfile(file, path[path.index("/")+1:])

            self.update_size()
            return message

    def __add_subfile(self, file, path=""):
        """
        Serves as a recursive helper function to the add_file method.

        Inputs:
            file (File): a file object to add to the directory's list of files
            path (str, optional): subdirectory to add file to; if not specified,
                file will be added to current directory

        """
        if path == "":
            if file not in self.files:  # prevents duplicate files
                self.files.append(file)
                self.__size += file.size
                return "SUCCESS: File successfully added"
            else:
                return "ERROR: File already exists"

        # recursively traverse to correct directory
        else:
            new_dir = path[:path.index("/")]
            new_path = path[path.index("/")+1:]

            new_dir_idx = self.subdirectories.index(Directory(new_dir))
            return self.subdirectories[new_dir_idx].__add_subfile(file, new_path)

    def add_directory(self, directory, path=""):
        """
        Adds a subdirectory to a directory.

        Inputs:
            directory (Directory): a directory object to add to the
                specified path's list of subdirectories
            path (str, optional): subdirectory to add directory to; if not 
                specified, directory will be added to current directory

        Return:
            (str): message if directory was successfully added
        """

        exists, obj_type = self.path_exists(path)

        if not exists:
            return "ERROR: Path does not exist"

        elif obj_type == "file":  # can't add a directory to a file
            return "ERROR: Cannot add a directory to a File"

        else:
            message = ""
            if path == "":
                message = self.__add_subdir(directory, path)

            # remove main
            else:
                message = self.__add_subdir(
                    directory, path[path.index("/")+1:])

            self.update_size()
            return message

    def __add_subdir(self, directory, path=""):
        """
        Serves as a recursive helper function to the add_file method.

        Inputs:
            file (File): a file object to add to the directory's list of files
            path (str, optional): subdirectory to add file to; if not specified,
                file will be added to current directory

        """

        if path == "":
            if directory not in self.subdirectories:  # prevents duplicate files
                self.subdirectories.append(directory)
                self.__size += directory.__size
                return "SUCCESS: Directory was successfully added"
            else:
                return "ERROR: Directory already exists"

        # recursively traverse to the correct directory
        else:
            new_dir = path[:path.index("/")]
            new_path = path[path.index("/")+1:]

            new_dir_idx = self.subdirectories.index(Directory(new_dir))
            self.subdirectories[new_dir_idx].__add_subdir(directory, new_path)

    def remove(self, path):
        """
        Removes a file or a subdirectory from a directory.

        Inputs:
            locaion (int, optional): the location of the file to remove; if
                unspecified, removes the file at the 0-index.

        Returns:
            (int): the size of the removed file, -1 if error
        """

        exists, _ = self.path_exists(path)
        if (not exists) or (path == ""):
            print("ERROR: File does not exist")
            return -1

        else:
            # removing main dir
            return self.__remove_obj(path[path.index("/")+1:])

    def __remove_obj(self, path):
        """
        Helper function for removing an object (file or directory) for a 
            Directory object

        Inputs:
            path (str): path of object (file or directory) to remove

        Returns:
            (int): 1 if the object was successfully removed, -1 otherwise
        """

        removed = 0

        # removing a file
        if "/" not in path:
            remove_idx = self.files.index(File(0, path))
            removed = self.files.pop(remove_idx).size

        # traversing a sub-directory
        else:
            new_dir = path[:path.index("/")]
            new_path = path[path.index("/")+1:]

            # remove a directory
            if new_path == "":
                dir_idx = self.subdirectories.index(Directory(new_dir))
                removed = self.subdirectories.pop(dir_idx).__size

            # recursively traverse to subdirectory or sub-file
            else:
                dir_idx = self.subdirectories.index(Directory(new_dir))
                removed = self.subdirectories[dir_idx].__remove_obj(new_path)

        self.__size -= removed
        return removed

    def update_size(self):
        """
        Updates the size of the main directory and it's subdirectories, where
            the size of each directory is equal to the sum of the sizes of each 
            files in the directory

        Returns:
            (int) size of the directory
        """

        size = 0

        # get a count of all of the files
        for file in self.files:
            size += file.size

        # get a count of all the files in the subdirectories
        for subdir in self.subdirectories:
            size += subdir.update_size()

        self.__size = size
        return self.__size

    def get_file(self, path):
        """
        Gets the file at the stated path.

        Inputs:
            path (str): the path where the file resides.

        Returns:
            (File): file object at the path
                if the path doesn't exist, returns None.
        """

        exists, type = self.path_exists(path)

        if (not exists) or (type != "file"):
            return None

        return self.__get_subfile(path[path.index("/")+1:])  # remove main

    def __get_subfile(self, path):
        """
        Helper function to get file.

        Inputs:
            path (str): the path where the file resides.

        Returns:
            (File): file object at the path
                if the path doesn't exist, returns None.
        """

        if "/" not in path:  # base case - we've reached the file name
            file_idx = self.files.index(File(0, path))
            return self.files[file_idx]

        # recursively traversing to file location
        new_path = path[path.index("/")+1:]
        new_dir = path[:path.index("/")]

        dir_idx = self.subdirectories.index(Directory(new_dir))
        return self.subdirectories[dir_idx].__get_subfile(new_path)

    def get_directory(self, path):
        """
        Gets the file at the stated path.

        Inputs:
            path (str): the path where the file resides.

        Returns:
            (File): file object at the path
        """

        exists, type = self.path_exists(path)

        if (not exists) or (type != "directory"):
            return None

        return self.__get_subdirectory(path[path.index("/")+1:])  # remove main

    def __get_subdirectory(self, path):
        """
        Helper function to get subdirectory.

        Inputs:
            path (str): the path where the subdirectory resides.

        Returns:
            (Directory): subdirectory object at the path.        
        """

        if (path == ""):
            return self

        new_path = path[path.index("/")+1:]
        subdir = path[:path.index("/")]
        subdir_idx = self.subdirectories.index(Directory(subdir))

        if (new_path == ""):
            return self.subdirectories[subdir_idx]

        else:
            return self.subdirectories[subdir_idx].__get_subdirectory(new_path)

    def num_files(self):
        """
        Determines the number of files within this directory.

        Returns:
            (int) count of file objects this directory contains
        """
        return len(self.files)

    def num_subdirectories(self):
        """
        Determines the number of subdirectories within this directory.

        Returns:
            (int) count of subdirectory objects this directory contains
        """
        return len(self.subdirectories)

    def get_size(self):
        """
        Returns the total size of the directory, where size is the sum of the
            sizes of each subdirectory and file.

        Returns:
            (int): size of current directory
        """

        return self.__size
