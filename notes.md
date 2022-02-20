### Limitations and observations
- gRPC Security: Provides auth via TLS.  Not tested.
- Written in C++ with bindings in all major languages.
- Provides async, so no need to wait on network failure.
- Also comes with protobuf which is a popular serialization mechanism.
- Have not tested it on anything other than localhost, should be trivial to
  test with dockers
