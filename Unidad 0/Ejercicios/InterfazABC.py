# Standard library imports
from abc import ABC, abstractmethod
from typing import Any


class EstructuraLineal(ABC):

    @abstractmethod
    def insertar(self, elemento: Any) -> None:
        """ Adds an element to the structure. """
        pass


    @abstractmethod
    def eliminar(self) -> Any:
        """ Removes and returns the top item in the structure."""
        pass


    @abstractmethod
    def esta_vacia(self) -> bool:
        """ Checks if the structure is empty. """
        pass


    @abstractmethod
    def __len__(self) -> int:
        """ Returns the number of items in the structure. """
        pass


# =======================================================================
# Class Pila (Stack) implementation
# ======================================================================
class Pila(EstructuraLineal):

    def __init__(self) -> None:
        """ Initializes an empty stack."""
        self.items: list[Any] = []

    
    def esta_vacia(self) -> bool:
            """
            Checks if the stack is empty.
    
            Returns:
                bool: True if the stack is empty, False otherwise.
            """
            return len(self.items) == 0

    
    def insertar(self, elemento: Any) -> None:
        """
        Adds an element to the top of the stack.

        Args:
            elemento (Any): The element to be added to the stack.
        """
        self.items.append(elemento)


    def eliminar(self) -> Any:
        """
        Removes and returns the top item in the stack.

        Returns:
            Any: The top item in the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if not self.esta_vacia():
            return self.items.pop()
        else:
            raise IndexError("pop from empty stack")

    
    def __len__(self) -> int:
        """
        Returns the number of items in the stack.

        Returns:
            int: The number of items in the stack.
        """
        return len(self.items)


    def peek(self) -> Any:
        """
        Returns the top item in the stack without removing it.

        Returns:
            Any: The top item in the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        if not self.esta_vacia():
            return self.items[-1]
        else:
            raise IndexError("peek from empty stack")


    def __str__(self) -> str:
        """
        Returns a string representation of the stack.

        Returns:
            str: A string representation of the stack.
        """
        return str(self.items)

# Example usage:
if __name__ == "__main__":
    # Create a stack and perform some operations
    stack = Pila()

    # add items to the stack
    stack.insertar(10)
    stack.insertar(20)
    stack.insertar(30)
    stack.insertar(40)

    # print the stack and its properties
    print("Stack:", stack)  # Output: Stack: [10, 20, 30, 40]
    print("Top item:", stack.peek())  # Output: Top item: 40
    print("Stack size:", len(stack))  # Output: Stack size: 4

    # remove the top item from the stack
    print("Popped item:", stack.eliminar())  # Output: Popped item: 40
    print("Stack after pop:", stack)  # Output: Stack after pop: [10, 20, 30]
    print("stack size after pop:", len(stack))  # Output: Stack size after pop: 3


print("---------------------------------------------------")
# =======================================================================
# Class Cola (Queue) implementation
# =======================================================================
class Cola(EstructuraLineal):

    def __init__(self) -> None:
        """ Initializes an empty queue."""
        self.items: list[any] = []
    
    
    def esta_vacia(self) -> bool:
        """
        Checks if the queue is empty.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        return len(self.items) == 0


    def insertar(self, elemento: any) -> None:
        """
        Adds an element to the end of the queue.

        Args:
            elemento (any): The element to be added to the queue.
        """
        self.items.append(elemento)


    def eliminar(self) -> any:
        """
        Removes and returns the first item in the queue.

        Returns:
            any: The first item in the queue.

        Raises:
            IndexError: If the queue is empty.
        """
        if not self.esta_vacia():
            return self.items.pop(0)
        else:
            raise IndexError("dequeue from empty queue")
        

    def __len__(self) -> int:
        """
        Returns the number of items in the queue.

        Returns:
            int: The number of items in the queue.
        """
        return len(self.items)

    def peek(self) -> any:
        """
        Returns the first item in the queue without removing it.

        Returns:
            any: The first item in the queue.
        """
        if not self.esta_vacia():
            return self.items[0]
        else:
            raise IndexError("peek from empty queue")

    def __str__(self) -> str:
        """
        Returns a string representation of the queue.

        Returns:
            str: A string representation of the queue.
        """
        return str(self.items)
    
# Example usage
if __name__ == "__main__":
    # Create a queue and perform some operations
    queue = Cola()
    
    # Enqueue items
    queue.insertar(10)
    queue.insertar(20)
    queue.insertar(30)
    queue.insertar(40)
    
    # Display the queue and its properties
    print("Queue:", queue)  # Output: Queue: [10, 20, 30, 40]
    print("Front item:", queue.peek())  # Output: Front item: 10
    print("Queue size:", len(queue))  # Output: Queue size: 4
    
    # Dequeue an item
    print("Dequeued item:", queue.eliminar())  # Output: Dequeued item: 10
    print("Queue after dequeue:", queue)  # Output: Queue after dequeue: [20, 30, 40]
    print("Queue size after dequeue:", len(queue))  # Output: Queue size after dequeue: 3