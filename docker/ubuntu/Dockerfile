FROM ubuntu:20.04
LABEL org.opencontainers.image.title="conan-ubuntu"
LABEL org.opencontainers.image.authors="Björn Stresing <bjoern.stresing@gmx.de>"
LABEL org.opencontainers.image.description="This image provides an environment with python & conan already installed"
LABEL org.opencontainers.image.source="https://github.com/Tereius/conan-azure-templates/tree/master/docker/ubuntu"
LABEL org.opencontainers.image.url="https://github.com/Tereius/conan-azure-templates/pkgs/container/conan-ubuntu"

RUN apt-get update && apt-get install -y python3 python3-pip sudo curl && apt-get clean && update-alternatives --install /usr/bin/python python /usr/bin/python3 1 \
 && apt-get autoremove -y && apt-get purge -y --auto-remove && rm -rf /var/lib/apt/lists/*
RUN useradd -d /home/conan -u 10000 conan
RUN echo 'conan ALL = NOPASSWD: /usr/bin/apt,/usr/bin/apt-get,/usr/bin/aptitude,/usr/bin/apt-fast' >> /etc/sudoers
RUN pip3 install conan==2.3.1

USER conan
WORKDIR /home/conan
COPY --chown=conan:conan --chmod=744 entrypoint.sh /
CMD ["bash"]
ENTRYPOINT ["/entrypoint.sh"]
