"""
CMP1902M Assessment Task 1

Import and read the given dictionary (txt file).
Implement an interval search algorithm (examples: binary search).
Ask the user for a search query.
Use the implemented algorithm to find the search query.
If found, return the number of line that the search query is located.
Perform error handling.

Typical usage example:
    search_obj = Search('legalise', 'words.txt')
    if search_obj.get_data():
        print(search_obj.search())
"""


class Task1:
    """Singleton search algorithm implementation.

    Class has two functions, (get_data) which prepares the data
    for the (search) function. The use of the Singleton allows for
    multiple instances to use different data.


    Attributes:
        query: A string containing the data looking to be found.
        filename: A string containing the name of the file wanted to be searched.
        data: A mutable list to store data imported from file.
    """

    def __init__(self, query: str, filename: str):
        """Inits object with 3 attributes"""
        self.data = []
        self.query = query
        self.filename = filename

    def get_data(self) -> bool:
        """imports words.txt/csv file into python list.
        
        Data is imported using the filename attribute string.
        the file type can be csv or txt where each new data entry is
        stored on a newline. Data stored in according attribute.

        """
        try:
            with open(self.filename, 'r', encoding="utf-8") as file:
                self.data = file.read().split()
                return True
        except FileNotFoundError:
            print("""Function (get_data) failed.
            Dependencies missing or script is running in incorrect location.""")

        return False


    def search(self) -> int | str:
        """Ternary search.

        Performs an iterative Ternary search that divides the list into 3 parts,
        and compares the data to each section. This algorithm takes fewer loops
        to complete than a binary search, although more comparisons each loop.

        Returns:
            An integer that indicates which line the data is found.

        Raises:
            RuntimeError: When the data is not imported or search term is not found.
        """
        
        if not self.data:
            raise RuntimeError("variable (data) is empty, please call function get_data")

        start = 0
        end = len(self.data)

        while end >= start:

            third_1 = start + (end - start) // 3
            third_2 = end - (end - start) // 3

            if self.data[third_1] == self.query:
                return third_1 + 1

            if self.data[third_2] == self.query:
                return third_2 + 1

            # Check which third the value is in.

            if self.data[third_1] > self.query:
                # The value is in T1.
                end = third_1 - 1

            elif self.data[third_1] < self.query < self.data[third_2]:
                # The value is in the T2.
                start = third_1 + 1
                end = third_2 - 1

            else:
                # The value is in T3.
                start = third_2 + 1

        # The data is not found.
        return 0


if __name__ == "__main__":
    search_obj = Task1('legalise', 'words.txt')
    if search_obj.get_data():
        print(search_obj.search())
        # outputs 32599.
