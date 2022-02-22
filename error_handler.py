import functools
import platform
import traceback
import sys
import botocore.exceptions

def exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # pylint: disable=import-outside-toplevel
        from botocore.client import ClientError
        from botocore.exceptions import UnknownServiceError
        from boto3 import __version__ as boto3_version

        try:
            return func(*args, **kwargs)

        except ClientError as e:
            message = "\nO serviço {} não existe nessa região".format(
                    func.__qualname__
                )
            print(message)
        
        except botocore.exceptions.ProfileNotFound as e:
            message = "\nO profile informado não existe"
            print(message)

        except UnknownServiceError:
            print("Atualize sua versão do boto3 para a mais recente.")

            issue_info = "\n".join(
                (
                    "Python:        {0}".format(sys.version),
                    "boto3 version: {0}".format(boto3_version),
                    "Platform:      {0}".format(platform.platform()),
                    "",
                    traceback.format_exc(),
                )
            )
            print(issue_info)

        except Exception: 
            print("Você achou um bug, abra um PR no nosso projeto")

            issue_info = "\n".join(
                (
                    "Python:        {0}".format(sys.version),
                    "boto3 version: {0}".format(boto3_version),
                    "Platform:      {0}".format(platform.platform()),
                    "",
                    traceback.format_exc(),
                )
            )
            print(issue_info)

    return wrapper