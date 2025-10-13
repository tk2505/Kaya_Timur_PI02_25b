// Создание мультисписка (вложенного списка):
public class Node {
    int data;
    Node prev;
    Node next;

    public Node(int data)
    {
        this.data = data;
        this.prev = null;
        this.next = null;
    }
}

public class DoublyLinkedList {
    Node head;
    Node tail;

    public DoublyLinkedList()
    {
        this.head = null;
        this.tail = null;
    }
}

// Создание очереди:
Queue<String> queue = new LinkedList<>();
queue.add("банан"); 
queue.add("яблоко"); 
queue.add("ананас"); 

//Создание дека:
Deque<Integer> stack = new ArrayDeque<>();
stack.push(1); 
stack.push(2); 
stack.push(3); 

//Создание приоритетной очереди:
PriorityQueue<Integer> minHeap = new PriorityQueue<>();
minHeap.offer(10); 
minHeap.offer(5); 
minHeap.offer(15); 
minHeap.offer(2); 

//Создание приоритетной очереди с компаратором:
PriorityQueue<Task> priorityQueue = new PriorityQueue<>(idComparator);
priorityQueue.add(new Task(10001, "Task 1", 5)); 
priorityQueue.add(new Task(10003, "Task 3", 10)); 
priorityQueue.add(new Task(10002, "Task 2", 1)); 


