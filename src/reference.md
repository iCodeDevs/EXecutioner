## SNIPPETS

- To run subprocess and get continous output
```python
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=1)
for line in iter(p.stdout.readline, b''):
    print line,
p.stdout.close()
p.wait()
```