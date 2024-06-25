FROM tobix/pywine:3.12
MAINTAINER Björn Stresing <bjoern.stresing@gmx.de>

RUN useradd -d /home/conan -u 23100 conan
RUN wine64 pip install conan==2.3.1

USER conan
WORKDIR /home/conan
COPY --chown=conan:conan --chmod=744 entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
