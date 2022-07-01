FROM archlinux:latest

ENV LANG=en_US.UTF-8
CMD ["/usr/bin/bash"]

# Initialise dir(s)
RUN mkdir /app
ADD . /app
WORKDIR /app

# Install all required packages
COPY install_deps.sh /tmp/
RUN bash /tmp/install_deps.sh