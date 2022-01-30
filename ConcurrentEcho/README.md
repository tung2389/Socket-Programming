# Different implementations of the echo applications.

Different implementations of the echo applications, including a simple server that can only handle one connection at a time, and multiple implementations of concurrent server using process, I/O multiplexing and multiple threads. The code samples are from the CS:APP3e website: http://csapp.cs.cmu.edu/3e/code.html


## Usage

The server directory contains the code for 4 different implementations of an echo server:
1. The most simple echo server, which can only handle one client at a time. Build using command ```make echoIterative```.
2. This server achieves concurrency by forking a dedicated process to serve each client. Build by ```make echoProcess```.
3. This server uses I/O multiplexing with select() function to handle multiple connections. Build by ```make echoIOMultiplex```.
4. This server spanws a new thread to handle each new client. Build by ```make echoThread```.

## Comparisons between different methods of achieving concurrency:

1. Forking new processes to handle each new connection:
- Pros:
    - Simple.
    - Having seperate address spaces for different processes.
- Cons:
    - High overhead for process control.
    - Hard to share resources between processes.

2. I/O Multiplexing:
- Pros:
    - One logical control flow and address space, easily for debugging with a debugger.
    - No overhead for process or thread control.
- Cons:
    - Significantly more complex to code than process-based or thread-based design.
    - Hard to provide fine-grained concurrency. As granularity of the concurrency decreases, the complexity of the code grows.
    - Cannot take advantage of multi-core processors.

3. Using multiple threads:
- Pros:
    - Easy to share data between threads.
    - Lower over-head compare to process-based designs.
- Cons:
    - Must be careful to avoid unintended sharing, which introduce subtle and hard-to-produce error.
    - All functions called by a thread must be thread-safe.
