# Home Assistant LDAP Auth

Simple script to have LDAP authentication in Home Assistant Docker, using [NGINX's ldap-auth container](https://github.com/nginxinc/nginx-ldap-auth).

## Usage
* Deploy NGINX's ldap-auth container
* Put the script and config file in the Home Assistant config directory
* Adjust config file to match your environment
* Configure [Home Assistant auth provider](https://www.home-assistant.io/docs/authentication/providers/)
    ```yaml
    auth_providers:
        - type: command_line
          name: 'LDAP'
          command: '/usr/local/bin/python3'
          args: ['/config/ldap-auth.py', '/config/ldap-auth.yaml']
          meta: false
    ```
* Restart Home Assistant

## Configuration
The following options are available:
| Name | Description |
| --- | --- |
| auth-url | URL where the ldap-auth server can be found |
| ldap-url | URL for the LDAP server (scheme://host:port) |
| ldap-basedn | The Base DN to search for users |
| ldap-binddn | The DN to use for binding to the directory (leave empty for anonymous binding) |
| ldap-bindpass | The password for the configured Bind DN |
| ldap-template | Template to find the user in the directory |
| ldap-starttls | Wether to enable TLS encryption on the LDAP connection |
| ldap-realm | The LDAP realm name |

See [this documentation](https://github.com/nginxinc/nginx-ldap-auth#installation-and-configuration) for more information on possible values and defaults.

## Under the hood
The NGINX ldap-auth container is controlled by sending specific headers that are sent with the authentication request. The script will set these headers with the values from the config files. Home Assistant will start the script with the username and password in environment variables, which are used as basic auth credentials to send a request to the auth-url. The ldap-auth container will in its turn verify the credentials at the LDAP server. If the credentials are correct, it will respond with HTTP code 200, otherwise 401. Based on this response code, the script will exit with or without an error so Home Assistant allows the user to enter or not.

## Disclaimer
This was written for personal use, to re-enable LDAP authentication in the Home Assistant Docker image, which lacks the Python LDAP module as well as LDAP support in curl. There's hardly any error handling and I am in no way responsible for any security issues caused by the use of this script. Misconfigurations *can* expose your Home Assistant installation to malicious people.

NGINX **does not** supply Docker images for their container. Please note that someone else's image from a repository could expose your Home Assistant and/or leak your credentials so I'd recommend you to build your own.
