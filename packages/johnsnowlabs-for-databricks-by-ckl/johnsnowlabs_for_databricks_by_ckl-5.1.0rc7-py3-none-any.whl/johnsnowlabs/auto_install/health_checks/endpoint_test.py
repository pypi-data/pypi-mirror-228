lic = """
{
  "SPARK_OCR_LICENSE": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTYwMzE5OTksImlhdCI6MTY5MzM1MzYwMCwidW5pcXVlX2lkIjoiNzRjNTY2M2MtNDczYy0xMWVlLWJkMDYtYmE5YmQ4NmY0MWRjIiwic2NvcGUiOlsib2NyOmluZmVyZW5jZSIsIm9jcjp0cmFpbmluZyIsImhlYWx0aGNhcmU6aW5mZXJlbmNlIiwiaGVhbHRoY2FyZTp0cmFpbmluZyJdLCJwbGF0Zm9ybSI6eyJuYW1lIjoiRGF0YWJyaWNrcyIsImluc3RhbmNlX3VybCI6Imh0dHBzOi8vYWRiLTM3ODQ4MDA4NDIyNTg4OTQuMTQuYXp1cmVkYXRhYnJpY2tzLm5ldCIsIm9yZ2FuaXphdGlvbl9pZCI6IjM3ODQ4MDA4NDIyNTg4OTQifX0.YUPZChPvMB6vc1xWrD7vE8UUZSEH4H2aW3sNxhZmMIpkra5-bE1VTCfVSMB_UKynRA-zVOAuAsdcgVEPJRX3hp57RKTKuOnOZIY4MlqkMxRf9yM2W3Ddj8EhV5dFZD_zJBuCFAiewaslvY7G0otWeAvcCi9SxkQuNprXNPl5FWAyoCqg-7vfrZJl8rybaHsd1ot3jteapLdTJcZEYYjKi1O7iqBcWMbN1CFb0eHoqtGJkm9jqFkP1s6kt24Ed_Rd03O5iNRvxGmZ6kNOPy60nBwfMz7XkVGrgaw58Gt3iiW8Sq-MpFPVIrBm1eQ44fqRlzoT3GbwXl3OCYoF3SK0ig",
  "SPARK_OCR_SECRET": "5.0.0-9fd5dda7491d999a05c9bdac4b92a046694e8116",
  "OCR_VERSION": "5.0.0",
  "SPARK_NLP_LICENSE": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTYwMzE5OTksImlhdCI6MTY5MzM1MzYwMCwidW5pcXVlX2lkIjoiNzRjNTY2M2MtNDczYy0xMWVlLWJkMDYtYmE5YmQ4NmY0MWRjIiwic2NvcGUiOlsib2NyOmluZmVyZW5jZSIsIm9jcjp0cmFpbmluZyIsImhlYWx0aGNhcmU6aW5mZXJlbmNlIiwiaGVhbHRoY2FyZTp0cmFpbmluZyJdLCJwbGF0Zm9ybSI6eyJuYW1lIjoiRGF0YWJyaWNrcyIsImluc3RhbmNlX3VybCI6Imh0dHBzOi8vYWRiLTM3ODQ4MDA4NDIyNTg4OTQuMTQuYXp1cmVkYXRhYnJpY2tzLm5ldCIsIm9yZ2FuaXphdGlvbl9pZCI6IjM3ODQ4MDA4NDIyNTg4OTQifX0.YUPZChPvMB6vc1xWrD7vE8UUZSEH4H2aW3sNxhZmMIpkra5-bE1VTCfVSMB_UKynRA-zVOAuAsdcgVEPJRX3hp57RKTKuOnOZIY4MlqkMxRf9yM2W3Ddj8EhV5dFZD_zJBuCFAiewaslvY7G0otWeAvcCi9SxkQuNprXNPl5FWAyoCqg-7vfrZJl8rybaHsd1ot3jteapLdTJcZEYYjKi1O7iqBcWMbN1CFb0eHoqtGJkm9jqFkP1s6kt24Ed_Rd03O5iNRvxGmZ6kNOPy60nBwfMz7XkVGrgaw58Gt3iiW8Sq-MpFPVIrBm1eQ44fqRlzoT3GbwXl3OCYoF3SK0ig",
  "SECRET": "5.0.2-2edb671dfc23389dc2b428f9c49244415b340f34",
  "JSL_VERSION": "5.0.2",
  "PUBLIC_VERSION": "5.0.2",
  "AWS_ACCESS_KEY_ID": "ASIASRWSDKBGHDGOGEM5",
  "AWS_SECRET_ACCESS_KEY": "VhhresMiHrEZiEZz6sPsIx43h0etwO6hWzYF814y",
  "AWS_SESSION_TOKEN": "IQoJb3JpZ2luX2VjEPb//////////wEaCXVzLWVhc3QtMSJHMEUCIF3YCO7ijf9gHEaPFRLTfzWis/P0VXaNYHP0buD6QmKjAiEAwnQLir3AXAVeYHPUprAJg9Wk/yaFQp93p1uSfzJ3H4wq0wIIv///////////ARAEGgwxNzU0NjA1MzYzOTYiDHvK7GCBoErFgHdCYiqnAplAVHIKWD6ThbaukqiDpVnCTHru3kMccS6EY9oUTlehwMeYi1rrKQrRxvafaQTXVYHXkmy0iytYgF6za5LxIJY7SCIBlx5iy9/RTgDyDXzNHh5cWGpcngZXqn4kDo2iBlEpMAl3HK7iVpJ61cqkztcifIjrulYc2vwHDGf6PP1WuP6UKCOQRD6n2MYEyQKV+1YJLunJ2+RPRfMgZ7+OGSuRjl4gnMaqY5yIy0WA4o0aLjJE2JJFXT0m1mw9apA7ym4yMkIfsKd+3xK8dgHdyN8VxTh1AiVhb81Hpg8Md0t9tw6aS3jaFv1wpYE9xpSSIjPyu2XWDeHYKcpBZ+LvNpzshisTDSp/LKhpGuJOePorYpgY1v4KUFJTL1OWtnTD+tq//qT0nJUwvpO9pwY61wGUbXqNKKZQ4ZMahRa4gSivwFLOTogF4RO0GlVmRD2MtH4IPDcXShOjkdiAQ1352vwWT/9UxQKLQ+YJnhLvy85M7w0fwD9XjkbGiGqVjUoeyRR338tbfTKQYBxz6ay2HPqAUTleX5xEyqshazmhphX/MDdbrgaaj+0+cVFf7A6CP7G59xMRbcACBjU6zv3iLNtzChug+FQY6c0Y6bx2UyCrRejfc+rA5ykqsz2jl2aHkDw4grn5Zleg9vDtPaWJQAv7ak4slBEXXSJDc+p5sbgvC5mpnjEU1Q=="
}
"""
import mlflow

from johnsnowlabs.auto_install.databricks.endpoints import *


def new_req():
    from mlflow.utils.requirements_utils import _get_pinned_requirement
    from johnsnowlabs import settings

    _SPARK_NLP_JSL_WHEEL_URI = (
        "https://pypi.johnsnowlabs.com/{secret}/spark-nlp-jsl/spark_nlp_jsl-"
        + f"{settings.raw_version_medical}-py3-none-any.whl"
    )

    return [
        f"johnsnowlabs_for_databricks_by_ckl=={settings.raw_version_jsl_lib}",
        _get_pinned_requirement("pyspark"),
        _SPARK_NLP_JSL_WHEEL_URI.format(secret=os.environ["SECRET"]),
        "pandas<=1.5.3",
    ]


mlflow.johnsnowlabs.get_default_pip_requirements = new_req


def run_test():
    mlflow.set_experiment("/Users/christian@johnsnowlabs.com/my-experiment")
    os.environ["JOHNSNOWLABS_LICENSE_JSON_FOR_CONTAINER"] = lic
    os.environ["JOHNSNOWLABS_LICENSE_JSON"] = lic
    res = query_and_deploy_if_missing("tokenize", "Hello World", True, True)
    print(res)


if __name__ == "__main__":
    run_test()
