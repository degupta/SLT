protoc --go_out=pb/ --go_opt=paths=source_relative --go-grpc_out=pb/ --go-grpc_opt=paths=source_relative game.proto

python3 -m grpc_tools.protoc -I./ --python_out=pytest --pyi_out=pytest --grpc_python_out=pytest game.proto