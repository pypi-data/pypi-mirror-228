# edgepi-rpc-protobuf
Protobuf files for EdgePi RPC

## Importing raw files as npm package
```
npm install @edgepi-cloud/rpc-protobuf
```

## Importing python generated code
```
pip install edgepi-rpc-protobuf
```

## Compiling to other languages
- Install protobuf compiler (protoc) and install a protobuf runtime library for a supported language. Visit the [official repo](https://github.com/protocolbuffers/protobuf) for steps.
- Compile with the following command
```
protoc -I=. --<language>_out=. <proto_file_path>
```
In the command line, we trigger the protocol compiler using three arguments:

1. -I: Specifies the directory in which we look for necessary dependencies (we utilize "." which represents the present directory).
2. --python_out: Indicates the destination for generating a Python integration class (once again, we use "." for the current directory).
3. The final parameter without a name designates the .proto file that will undergo compilation.
