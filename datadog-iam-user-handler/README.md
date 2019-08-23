# Datadog::Users::User

To get started:

* Build [datadog-api-client-java](https://github.com/DataDog/datadog-api-client-java):

    ```
    git clone git@github.com:DataDog/datadog-api-client-java.git
    cd datadog-api-client-java
    # this will install the client into ~/.m2/repository
    mvn install -Dmaven.test.skip=true
    ```

* Build `datadog-cloudformation-common` from this repository:

    ```
    mvn -f ../datadog-cloudformation-common/pom.xml -Dmaven.test.skip=true install
    ```

* Install cfn-cli
* Do note that for now, the tests use `DD_TEST_CF_API_KEY` and `DD_TEST_CF_APP_KEY` from environment variables.
* Run `mvn test` inside this directory to invoke tests locally.
