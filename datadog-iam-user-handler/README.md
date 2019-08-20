# Datadog::Users::User

To get started:

* Build [datadog-api-client-java](https://github.com/DataDog/datadog-api-client-java):

    ```
    git clone git@github.com:DataDog/datadog-api-client-java.git
    cd datadog-api-client-java
    # this will install the client into ~/.m2/repository
    mvn install -Dmaven.test.skip=true
    ```

* Install cfn-cli
* Do note that for now, the resource uses `DATADOG_API_KEY` and `DATADOG_APP_KEY` from environment variables.
* Run `mvn test` inside this directory to invoke tests locally.