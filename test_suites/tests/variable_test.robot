*** Settings ***
Test Template  Run Keyword
*** Variables ***
${argument1}    default argument1
${argument2}    default argument2
${secret_argument}    default secret_argument

*** Test Cases ***
${argument1}    Log value with ${argument1}
${argument2}    Log value with ${argument2}
${secret_argument}    Log value with ${secret_argument}


*** Keywords ***
Log value with ${argument}
    Log    ${argument}
    Set Test Documentation    ${argument}
