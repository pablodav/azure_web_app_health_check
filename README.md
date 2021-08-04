Description
===========

Checks azure apps health.

`VERSION  <azure_web_app_health_check/VERSION>`__

Plugins input URL and key.
URL example: https://domainname.net/

The plugin will automatically add this to the url:

https://domainname.net/healthy?key=keyname

plugin expects return from webapp:

´´´json
{
  "status": "Healthy",
  "totalDuration": "00:00:02.9700420",
  "entries": {
    "process_health_check": {
      "data": {},
      "description": "Process health check was successful.",
      "duration": "00:00:02.9326800",
      "status": "Healthy"
    }
  }
}
´´´

Plugin will check the .status key is "Healthy" to return OK if not "CRITICAL".

Plugin will also output msg with .entries.description.

TODO:
plugin performance data: .totalDuration

Install
=======

Linux::

    sudo pip3 install azure_web_app_health_check --upgrade

Also is possible to use::

    sudo python3 -m pip install azure_web_app_health_check --upgrade

On windows with python3.5::

    pip install azure_web_app_health_check --upgrade

For proxies add::

    --proxy='http://user:passw@server:port'

Usage
=====

Use the command line::

    > azure_web_app_health_check --help
      usage: azure_web_app_health_check [-h] [-u [URL]] [-k [KEY]][-e [EXTRA_ARGS]]

        optional arguments:
        -h, --help            show this help message and exit
        -u [URL], --url [URL]
                              url to check 		
        -k [KEY], --key [KEY]
                              key for azure app 	
        -e [EXTRA_ARGS], --extra_args [EXTRA_ARGS]
                              extra args


Example usage
=============

Example use:

    > azure_web_app_health_check -u "https://xxx/" --key "pbxh1u3lcxgdfd22fhttjm17q"


Nagios config
=============

Example command::

    define command{
        command_name  azure_web_app_health_check
        command_line  /usr/local/bin/azure_web_app_health_check -u "$ARG1$" -k "$ARG2$" --extra_args='$ARG6$'
    }

Example service::

    define service {
            host_name                       SERVERX
            service_description             service_name
            check_command                   azure_web_app_health_check!http://url/!key
            use				                generic-service
            notes                           some useful notes
    }

You can use ansible role that already has the installation and command: https://github.com/CoffeeITWorks/ansible_nagios4_server_plugins


