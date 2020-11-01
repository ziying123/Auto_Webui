python3 -m pytest --alluredir Outputs/allure --clean-alluredir

allure generate Outputs/allure -c -o allure-report

allure open allure-report