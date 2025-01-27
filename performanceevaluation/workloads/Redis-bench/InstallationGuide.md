# Redis Benchmark Installation and Usage

## Introduction
`redis-benchmark` is a tool to perform various types of benchmarking for Redis, such as:
1. **SET/GET Operation Testing**: Evaluate Redis's read and write performance by executing `SET` and `GET` commands.
2. **Concurrent Connection Testing**: Simulate multiple concurrent connections to test Redis's performance under high-concurrency conditions.
3. **Multithreading Testing**: Test Redis's performance in a multi-threaded environment.
4. **Data Size Testing**: Evaluate Redis's performance when handling operations with varying data sizes.

## Installation
Redis Benchmark is included with the Redis installation. To install Redis:
1. Download and build Redis:
   ```bash
   wget http://download.redis.io/releases/redis-6.2.6.tar.gz
   tar xzf redis-6.2.6.tar.gz
   cd redis-6.2.6
   make
   ```
2. Verify `redis-benchmark` is available:
   ```bash
   ./src/redis-benchmark --help
   ```

## Basic Usage
Below are common examples of using `redis-benchmark` for performance testing.

### Example 1: High Concurrency Test
Run a test with 100 concurrent connections and 100,000 total requests:

```bash
redis-benchmark -h 127.0.0.1 -p 6379 -c 100 -n 100000
```

- **`-h 127.0.0.1`**: Redis server host (default is localhost).
- **`-p 6379`**: Redis server port (default is 6379).
- **`-c 100`**: Number of concurrent connections.
- **`-n 100000`**: Total number of requests to execute.

### Example 2: Silent Mode and Database Selection
Run a test targeting database 100 with summarized output:

```bash
redis-benchmark -h 127.0.0.1 -p 6379 -q -d 100
```

- **`-q`**: Run the benchmark in silent mode (outputs summary only).
- **`-d 100`**: Specify the database number to use (default is database 0).

### Example 3: SET and LPUSH Commands
Run 100,000 requests testing `SET` and `LPUSH` operations:

```bash
redis-benchmark -t set,lpush -q -n 100000
```

- **`-t set,lpush`**: Specify the command types to test (`SET` and `LPUSH` in this case).
- **`-q`**: Silent mode (outputs summary only).
- **`-n 100000`**: Total number of requests to execute.

### Example 4: Lua Script Performance
Run 100,000 requests executing a Lua script:

```bash
redis-benchmark -n 100000 -q script load "redis.call('set','foo','bar')"
```

- **`script load`**: Executes a Lua script in Redis.
- **Script Content**: `redis.call('set','foo','bar')` sets a key-value pair (`foo=bar`).

## Performance Metrics
The following metrics are included in the test results:
1. **Throughput**: The number of requests processed per second (e.g., `78802 requests/second`).
2. **Latency**: Average response time per request.
3. **Command Types**: Performance of individual Redis commands or Lua scripts.

## Conclusion
`redis-benchmark` is a versatile tool to evaluate Redis's performance under various conditions. Use it to test your setup, optimize configurations, and ensure Redis meets your application's demands.
```