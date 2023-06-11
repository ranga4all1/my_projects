from prefect_email import EmailServerCredentials


def create_email_creds_block():
    credentials = EmailServerCredentials(
        username="EMAIL-ADDRESS-PLACEHOLDER",
        password="PASSWORD-PLACEHOLDER",  # must be an app password
    )
    credentials.save("BLOCK-NAME-PLACEHOLDER", overwrite=True)


if __name__ == "__main__":
    create_email_creds_block()
