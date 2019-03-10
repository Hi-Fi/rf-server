*** Variables ***
${argument1}    default argument1
${argument2}    default argument2

*** Test Cases ***
First case from test1
    Log    Executing test case with argument ${argument1}

Second case from test1
    Log    Executing failing test case ${argument2}
    Fail
