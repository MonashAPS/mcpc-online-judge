FROM python:3.11-slim-bullseye

RUN printf '%s\n' \
        'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/20260901T000000Z bullseye main' \
        'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian-security/20260901T000000Z bullseye-security main' \
        'deb [check-valid-until=no] http://snapshot.debian.org/archive/debian/20260901T000000Z bullseye-updates main' \
        > /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        texlive-binaries texlive-latex-base texlive-latex-extra texlive-latex-recommended \
        texlive-pictures texlive-pstricks librsvg2-bin xxd imagemagick dvisvgm git && \
    rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/DMOJ/texoid/
WORKDIR /texoid/
RUN pip3 install -e .

EXPOSE 8888
ENTRYPOINT texoid --address=texoid --port=8888
