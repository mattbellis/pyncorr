Build with 

```
sh build .sh 
```

################################################################################
# Timing
################################################################################

# On my desktop
```
time ./fill 100000000
```
~10 seconds to do 100 million entries
~100 seconds to do 1 billion entries

Extrapolating
28 hours to do 1 trillion entries


# On my laptop
```
time ./fill 100000000
```
~17 seconds to do 100 million entries
~170 seconds to do 1 billion entries

Extrapolating
48 hours to do 1 trillion entries
