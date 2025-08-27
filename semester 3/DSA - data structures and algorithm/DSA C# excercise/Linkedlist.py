class Node:
    """Class to represent a node in the linked list."""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Class to represent the linked list."""
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, new_data):
        """Insert a new node at the beginning of the list."""
        new_node = Node(new_data)
        new_node.next = self.head
        self.head = new_node

    def delete_node(self, key):
        """Delete the first occurrence of a node with the given key."""
        temp = self.head

        # If the head node itself holds the key
        if temp is not None:
            if temp.data == key:
                self.head = temp.next
                temp = None
                return

        # Search for the key to be deleted
        prev = None
        while temp is not None:
            if temp.data == key:
                break
            prev = temp
            temp = temp.next

        # Key was not present in the list
        if temp == None:
            return

        # Unlink the node from the linked list
        prev.next = temp.next
        temp = None

    def traverse(self):
        """Print the linked list."""
        temp = self.head
        while temp:
            print(temp.data)
            temp = temp.next

# Example usage:
llist = LinkedList()
llist.insert_at_beginning(10)
llist.insert_at_beginning(20)
llist.insert_at_beginning(30)

llist.traverse()
# Output: 30, 20, 10

llist.delete_node(20)
llist.traverse()
# Output: 30, 10
