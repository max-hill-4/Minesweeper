"""
CMP1902M Assessment Task 1

• Import and read the given dictionary (txt file)
• Implement an interval search algorithm (examples: binary search)
• Ask the user for a search query
• Use the implemented algorithm to find the search query
• If found, return the number of line that the search query is located
• Perform error handling
"""


class Search:
    """Class that """
    def __init__(self, query:str, filename: str):
        self.data = []
        self.query = query
        self.filename = filename
    
    def search(self) -> int|str:
        """Iterative ternary search"""
        if not self.data:
            return "variable (data) is empty, please call function get_data"

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
                # The value is in T1
                end = third_1 - 1

            elif self.data[third_1] < self.query < self.data[third_2]:
                # The value is in the T2
                start = third_1 + 1
                end = third_2 - 1

            else:
                # The value is in T3
                start = third_2 + 1

        return "data was not found."

    def get_data(self) -> bool:
        """Maps words.txt/csv file to a python list, returning True if completed."""
        try:
            with open(self.filename, 'r', encoding="utf-8") as file:
                self.data = file.read().split()
                return True
        except FileNotFoundError:
            print("""Function (get_data) failed.
                    Dependencies missing or script is running in incorrect location.""")

        return False

if __name__ == "__main__":
    search_obj = Search('legalise', 'words.txt')
    if search_obj.get_data():
        print(search_obj.search())
