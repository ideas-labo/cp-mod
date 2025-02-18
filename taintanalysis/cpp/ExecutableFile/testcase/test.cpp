#include <iostream>


double add(double a, double b) {
    return a + b;
}


double subtract(double a, double b) {
    return a - b;
}


double multiply(double a, double b) {
    double result = 0.0;
    int b_int = static_cast<int>(b); 
    for(int i = 0; i < b_int; i++) {
        result += a;
    }
    return result;
}


double divide(double a, double b) {
    if (b == 0) {
        throw std::runtime_error("Division by zero error");
    }
    return a / b;
}

int main() {
    double num1, num2;
    
    std::cout << "Enter first number: ";
    std::cin >> num1;
    
    std::cout << "Enter second number: ";
    std::cin >> num2;


        // 加法
        std::cout << "Addition: " << num1 << " + " << num2 << " = " << add(num1, num2) << std::endl;
        
        // 减法
        std::cout << "Subtraction: " << num1 << " - " << num2 << " = " << subtract(num1, num2) << std::endl;
        
        // 乘法
        std::cout << "Multiplication: " << num1 << " * " << num2 << " = " << multiply(num1, num2) << std::endl;
        
        // 除法
        std::cout << "Division: " << num1 << " / " << num2 << " = " << divide(num1, num2) << std::endl;


    return 0;
}
