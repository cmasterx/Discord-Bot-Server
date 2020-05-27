#include <iostream>
#include <chrono>
#include <thread>

using namespace std;

int main()
{
    cout << "Starting Program!" << endl;
    
    unsigned long counter = 1;
    while (true) {
        cout << "Print! This is loop number " << counter << '\n';
        std::this_thread::sleep_for(std::chrono::seconds(1));
        ++counter;
    }
    
    return 0;
}