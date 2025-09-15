// создание списка на с++

#include <iostream>
#include <string>

int main() {
	std::string lst[] = {"РЭУ", "МГУ", "МИСИС"};
	int size = 3;

	for(int i = 0; i < size; i++) {
		std::cout << lst[i] << std::endl;
	}
	return 0;
}

// создание стека на с++
stack <string> stack;
stack.push("РЭУ");
stack.push("МГУ");
stack.push("МИСИС");