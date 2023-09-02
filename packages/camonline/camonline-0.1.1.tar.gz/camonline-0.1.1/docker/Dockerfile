FROM python:3.10.13-slim-bullseye

RUN apt-get update && apt-get install -y \
    tini ffmpeg x264 libx264-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install camonline

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["camonline", "start"]
