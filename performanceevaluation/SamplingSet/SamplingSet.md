# Sampling Data Set

## Format

| name                                 | valuename | value  |
| ------------------------------------ | --------- | ------ |
| yarn.dispatcher.drain-events.timeout | min       | 60000  |
| yarn.dispatcher.drain-events.timeout | default   | 600000 |
| yarn.dispatcher.drain-events.timeout | max       | 600000 |

Each table includes the configuration name, value name, and value size. The value name contains three types: min, max, and default. The test script reads one value each time, modifies it in the system, and then tests the performance indicators.
