FROM python:3-onbuild
MAINTAINER Rick Peters <rick.peters@me.com>

# make application directory available as volume
VOLUME /usr/src/app

# essential template resource not available in development build
# issue registered with mkdocs contributor
ADD search-results-template.mustache /usr/local/lib/python3.4/site-packages/mkdocs/assets/search/mkdocs/js/

ENV TZ Europe/Amsterdam
# since we use it as development container, default action is a shell
CMD [ "/bin/bash" ]
