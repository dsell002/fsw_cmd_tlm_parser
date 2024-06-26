#include <stdio.h>

// Define a structure with bit fields
struct Status {
    unsigned int isConnected : 1;
    unsigned int errorCode : 4;
    unsigned int reserved : 3;
};

// Define a structure
struct DataPacket {
    int id;
    float value;
    struct Status status;
};

// Define a union
union DataValue {
    int intValue;
    float floatValue;
    char strValue[20];
};

// Define a typedef
typedef unsigned long ulong;
typedef int (*FuncPtr)(int, float);

// Command function using a simple type
void CmdSetSpeed(int speed) {
    printf("Setting speed to %d\n", speed);
}

// Command function using a structure
void CmdProcessData(struct DataPacket data) {
    printf("Processing data: id = %d, value = %.2f\n", data.id, data.value);
}

// Command function using a union
void CmdHandleUnion(union DataValue value) {
    printf("Handling union value\n");
}

// Command function using a typedef
void CmdUseTypedef(ulong aliasValue) {
    printf("Using typedef alias value: %lu\n", aliasValue);
}

// Command function using a function pointer
void CmdUseFunctionPointer(FuncPtr func) {
    int result = func(10, 20.0f);
    printf("Function pointer result: %d\n", result);
}

// Example function for the function pointer
int ExampleFunction(int a, float b) {
    return a + (int)b;
}

int main() {
    // Example usage
    struct DataPacket packet = {1, 123.45, {1, 2, 0}};
    CmdProcessData(packet);

    union DataValue value;
    value.intValue = 42;
    CmdHandleUnion(value);

    CmdUseTypedef(1000UL);

    CmdUseFunctionPointer(ExampleFunction);

    return 0;
}
