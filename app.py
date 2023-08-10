import boto3
import webbrowser
import argparse
import os
import botocore.exceptions


def open_aws_console(profile, sso_url):
    session = boto3.Session(profile_name=profile)

    # Check if SSO credentials are needed
    if not sso_credentials_exist(session):
        authenticate_sso(profile)
        if not sso_credentials_exist(session):
            raise Exception("SSO authentication failed")

    # Open the URL with the obtained credentials
    webbrowser.open(sso_url)


def sso_credentials_exist(session):
    try:
        # This call will raise an exception if the credentials are not available
        session.client("sts").get_caller_identity()
        return True
    except (
        botocore.exceptions.BotoCoreError,
        botocore.exceptions.ClientError,
    ):
        return False


def authenticate_sso(profile):
    os.system(f"aws sso login --profile {profile}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Open AWS Console with Profile"
    )
    parser.add_argument("--profile", required=True, help="AWS profile name")
    args = parser.parse_args()

    sso_url = "https://aphexlog.awsapps.com/start#/"
    open_aws_console(args.profile, sso_url)
