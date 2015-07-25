FROM python:3-onbuild
MAINTAINER Rick Peters <rick.peters@me.com>

# make application directory available as volume
VOLUME /usr/src/app

ENV TZ Europe/Amsterdam
# since we use it as development container, default action is a shell
CMD [ "/bin/bash" ]
