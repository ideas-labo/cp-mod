**This directory contains the installation and deployment guides for all software, the deployment guides for benchmarks, and the Python files we use for performance testing.**

The artifact has been tested with Python 3.10. Ensure you have one of these versions installed.

### Performance test template:


```python

modify_config(config_file, parameter, value):
    stop_sys()

    # modify configuration value
    config.set(section, parameter, value)

    start_sys()

    if error occur:
        print(f"error：{error}")
        return False


stop_sys(){
	//stop system
}
   

start_sys(){
	//start system
}
  


run_bench(workload_factors):

    commands = {"your bench run command"}

    result = subprocess.run(command)
    return result.stdout



extract_metrics(bench_output):

    pattern = r"\\\\\"
    metric = pattern.bench_output

    return metric
	

clearconf(config_file):
    //change config file to default


    

main():

        config_file = "path to your config file"

        confdata = read_csv_to_dict("path to your test file")

        workload_factors = "your workload"


        for conf in confdata:
            clearconf(config_file)

            try:
                if(modify_config(config_file, conf['optionname'], conf['value']):
                    continue

                bench_output = run_bench(workload_factors)
                metric = extract_metrics(bench_output)

                results.append([conf['optionname'], conf['value'], metric)

            except Exception as e:
                print(f"---error---: {e}")
                continue
```