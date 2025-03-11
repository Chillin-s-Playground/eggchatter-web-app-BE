#!/bin/bash -e

tcps="test_create_profile_success"
tcpf="test_create_profile_failure"

_usage() {
  echo "Usage: $0 -s <test_file> -f <test_function_alias|all>"
  echo "Example: $0 -s users -f tcps"
  echo "         $0 -s users -f all"
  exit 1
}

while getopts "s:f:" opt; do
  case ${opt} in
    s)
      TEST_FILE=$OPTARG
      ;;
    f)
      TEST_FUNCTION_ALIAS=$OPTARG
      ;;
    *)
      _usage
      ;;
  esac
done

if [[ -z "$TEST_FILE" || -z "$TEST_FUNCTION_ALIAS" ]]; then
  _usage
fi

if [[ "$TEST_FUNCTION_ALIAS" == "all" ]]; then
  pytest "app/tests/${TEST_FILE}"
else
  TEST_FUNCTION=${!TEST_FUNCTION_ALIAS}
  if [[ -z "$TEST_FUNCTION" ]]; then
    echo "Invalid function alias: $TEST_FUNCTION_ALIAS"
    exit 1
  fi
  pytest "app/tests/test_${TEST_FILE}.py::$TEST_FUNCTION"
fi
