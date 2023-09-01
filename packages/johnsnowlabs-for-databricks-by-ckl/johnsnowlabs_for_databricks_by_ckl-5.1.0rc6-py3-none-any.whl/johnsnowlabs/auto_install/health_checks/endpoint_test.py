from johnsnowlabs.auto_install.databricks.endpoints import query_and_deploy_if_missing


def run_test():
    # spark.databricks.api.url
    query_and_deploy_if_missing("tokenize", "Hello World")


if __name__ == "__main__":
    run_test()
