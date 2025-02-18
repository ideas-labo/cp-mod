### Prerequisites

> openjdk 1.8.0_422
>
> javaparser 3.15.15

### JAVATools Indroduction

> **varsearch.java**: Search for the target variable initialization location and the location where it is called within the specified file.
>
> **controlflowsearch.java**: Search for the locations where control flow(while for switch if try) appears in the program.
>
> **functionsearch.java**: Search for the location where the target function is called an declared a java file.



### JAVATools Using



**controlflowsearch.java**

```java
// Input the folder path your need to analyse

String folderPath = "Your target folder";
```

Output result file will be `./controlflow_results.csv ` : 

| FilePath                                                     | controlflow | startline | endline |
| ------------------------------------------------------------ | ----------- | --------- | ------- |
| hadoop-3.3.5-src/hadoop-common-project/hadoop-common/src/test/arm-java/org/apache/hadoop/ipc/protobuf/TestRpcServiceProtosLegacy.java | switch      | 357       | 396     |
| hadoop-3.3.5-src/hadoop-common-project/hadoop-common/src/test/arm-java/org/apache/hadoop/ipc/protobuf/TestRpcServiceProtosLegacy.java | if          | 402       | 406     |
| hadoop-3.3.5-src/hadoop-common-project/hadoop-common/src/test/arm-java/org/apache/hadoop:/ipc/protobuf/TestRpcServiceProtosLegacy.java | switch      | 407       | 446     |



**varsearch.java**

```java
// Input the javafile path your need to analyze

String filePath = "java file path (.java) ";


// Input the variablename your need to analyze
String variableName = "Your variableName";
```

Output result file will be `./variable_results.csv ` : 

| variableName | declared or used | linenumber | Filepath |
| ------------ | ---------------- | ---------- | -------- |
|              |                  |            |          |
|              |                  |            |          |



**functionsearch.java**

```java
// Input the javafile path your need to analyze

String filePath = "java file path (.java) ";

// Input the functionname your need to analyze
String functionName = "Your functionname";
```

Output result file will be `./function_results.csv ` : 

| functionName | declared or called | linenumber | Filepath |
| ------------ | ------------------ | ---------- | -------- |
|              |                    |            |          |
|              |                    |            |          |





