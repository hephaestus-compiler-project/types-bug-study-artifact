FROM python:3
RUN pip3 install requests matplotlib pandas seaborn
RUN apt update -yqq && apt upgrade -yqq && apt install -yqq curl jq git \
    mercurial vim diffstat cloc

WORKDIR /home
