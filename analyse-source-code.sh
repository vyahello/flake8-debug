#!/usr/bin/env bash

# specifies a set of variables to declare files to be used for code assessment
PACKAGE="flake8_no_print"

# specifies a set of variables to declare CLI output color
FAILED_OUT="\033[0;31m"
PASSED_OUT="\033[0;32m"
NONE_OUT="\033[0m"


pretty-printer-box() {
:<<DOC
    Provides pretty-printer check box
DOC
    echo "Start ${1} analysis ..."
}


check-black() {
:<<DOC
    Runs "black" code analyser
DOC
    pretty-printer-box "black" && ( black --check ${PACKAGE} )
}


check-flake() {
:<<DOC
    Runs "flake8" code analysers
DOC
    pretty-printer-box "flake" && ( flake8 ${PACKAGE} )
}


check-tests() {
:<<DOC
    Runs "unit tests"
DOC
    pretty-printer-box "unit tests" && pytest
}


main() {
:<<DOC
    Runs "main" code analyser
DOC
    check-black && check-flake && check-tests
}

main