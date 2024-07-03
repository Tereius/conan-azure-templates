FROM tobix/pywine:3.12
LABEL org.opencontainers.image.authors="Björn Stresing <bjoern.stresing@gmx.de>"
LABEL org.opencontainers.image.title="conanwine"
LABEL org.opencontainers.image.description="This image provides a wine environment with python & conan already installed"
LABEL org.opencontainers.image.source="https://github.com/Tereius/conan-azure-templates/tree/master/docker/wine"

RUN useradd -d /home/conan -u 23100 conan
RUN wine64 pip install conan==2.3.1

USER conan
WORKDIR /home/conan
COPY --chown=conan:conan --chmod=744 entrypoint.sh /
CMD ["cmd"]
ENTRYPOINT ["/entrypoint.sh"]
