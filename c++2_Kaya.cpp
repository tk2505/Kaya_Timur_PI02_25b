// Создание мультисписка (вложенного списка):
struct Node {
    int data;
    Node *prev;
    Node *next;
};

// Создание очереди:
std::queue<std::string> queue;
queue.push("Tom"); 
queue.push("Bob"); 
queue.push("Sam");

//Создание дека:
std::deque<int> d = {1, 2, 3};

//Создание приоритетной очереди с примитивным типом:
std::priority_queue<int> pq;
pq.push(10);     
pq.push(20);    
pq.push(15); 

//Создание приоритетной очереди с пользовательскими структурами:
std::priority_queue<Task> taskQueue;
taskQueue.push({"Task 1", 2});     
taskQueue.push({"Task 2", 1});     
taskQueue.push({"Task 3", 3});  


