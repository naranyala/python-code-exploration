#include <thread>
#include <iostream>
#include <vector>

int main() {
	int n = 0;
	std::vector<std::thread> handles = {};
	for(int i=0; i<5; i++) {
    		handles.push_back(std::thread([&n]() {
        	for (int i=0; i<1000000; i++)
            	n++;
    	}));
	}
	for (auto& h : handles) {
    		h.join();
	}
	std::cout << n << "\n";
}
