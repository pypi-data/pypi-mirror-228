# IXON CDK Ingress

IXON CDK Ingress used in Custom Backend Components (CBC) for the IXON Cloud.

Learn more about how a machine builder can build their IoT portal using the IXON cloud on https://www.ixon.cloud/.

## ixapi-server repository testing image

The ixapi-server has an endpoint that will call a Custom Backend Components.
This functionality is tested in integration tests in the ixapi-server
repository which means that the ixapi-server requires a docker image of a CBC
that it can call.

To make sure that the ixapi-server supports the latest version of the IXON CDK
ingress, a docker image is created when this repository is tagged.  
The docker image that the ixapi-server uses is
`gitlab.ixon.net:4221/ixon/python/ixoncdkingress/ixoncdkingress-api-image:latest`
and is based on the `functions.py` and `requirements.py` in the `ixapiserverimage`
directory.
