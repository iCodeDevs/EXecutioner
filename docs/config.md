# CONFIG FILE FORMAT

```yaml

workspace: "playground" # the name of the folder inside which temporary files are created

languages: # Dictionary of objects for each programming language

# Format keys
# {filename} - the UUID name given for source code
# {source} - the formatted file name
# {compiled_file} - the formatted compiled file name
# {source_name} - the name of the source file excluding directory and extension

# Following comments which contain [] denote available format keys
    language_name:
        fileFormat: "" # filename format of the source code [filename]
        compileCommand: "" # the command used to compile the source file [source]
        executeCommand: "" # the command used to execute the compiled file [compiled_file]
        compiledFormat: "" # the filename format of the compiled code [source]
        disposible: # array of file formats that show files to be disposed after execution
            - ""
            - ""
        timeLimit: "" # time limit for execution (in seconds)
        memLimit: "" # memory limit for execution (in MB)
```
