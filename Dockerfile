FROM ubuntu:20.04

ENV TZ=Europe/Athens
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update -yqq && \
    apt upgrade -yqq && \
    apt install -yqq wget curl jq git sudo mercurial vim diffstat cloc python3-pip

RUN pip3 install requests matplotlib pandas seaborn

# Create a user.
RUN useradd -ms /bin/bash user && \
    echo user:user | chpasswd && \
    cp /etc/sudoers /etc/sudoers.bak && \
    echo 'user ALL=(ALL:ALL) NOPASSWD:ALL' >> /etc/sudoers
USER user

ENV HOME /home/user
WORKDIR ${HOME}
