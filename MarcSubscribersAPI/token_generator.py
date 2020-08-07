import shlex, subprocess, json


token_granting_configuration = {
    "super_username": "concepcion",
    "super_password": "marcpassword",
    "token_granting_url": "http://localhost:8000/o/token/",
    "client_id": "lLemOHWG0aXYTa9fRyTYBujLgIAO0qgxxBxFW6JI",
    "client_secret": "b2af93KvLTgH3oD4eNBAZbMnpnHOJxmyWpS7mrSXO3xm3lBzyeGIy9t3ose2onNPXYiWGunt99VYu10DqzuzHgtqj6nm5ejtvsCNOhK3d3UuZnA7Z2zPNZIHCwOBsA5E",
}


def generate_token():
    curl_command = "curl -X POST -d 'grant_type=password&username={username}&password={password}' -u{client_id}:{client_secret} {token_granting_url}" \
        .format(username=token_granting_configuration["super_username"],
                password=token_granting_configuration["super_password"],
                client_id=token_granting_configuration["client_id"],
                client_secret=token_granting_configuration["client_secret"],
                token_granting_url=token_granting_configuration["token_granting_url"])
    args = shlex.split(curl_command)
    process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    json_output = json.loads(stdout)
    if "access_token" not in json_output:
        raise TokenGrantingError
    token_value = json_output["access_token"]
    return token_value


class TokenGrantingError(Exception):
    pass
