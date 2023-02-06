FROM alpine:3.17

LABEL maintainer="software@sma.de"
LABEL vendor="SMA Solar Technology"

ARG SMA_USER=sma-user
ARG SMA_USERID=1000
ARG SMA_GROUP=sma
ARG SMA_GROUPID=1000

ARG SMA_RENDERING_HOME=/data

ENV SMA_RENDERING_HOME=${SMA_RENDERING_HOME}

RUN apk add --update --no-cache \
    python3 \
    py3-jinja2  \
    shadow && \
  rm -rf /var/cache/apt/* && \
  groupadd -g ${SMA_GROUPID} ${SMA_GROUP} && \
  useradd -c "${SMA_USER} user" -d /home/${SMA_USER} -u ${SMA_USERID} -g ${SMA_GROUPID} -m ${SMA_USER} && \
  chown -R ${SMA_USER}:${SMA_GROUP} /home/${SMA_USER} && \
  mkdir -p "${SMA_RENDERING_HOME}" && \
  chown ${SMA_USERID}:${SMA_GROUPID} "${SMA_RENDERING_HOME}"

USER ${SMA_USER}
ENV HOME /home/${SMA_USER}

COPY --chmod=755 sma-jinja-renderer.py /usr/bin/sma-jinja-renderer

VOLUME [ "${SMA_RENDERING_HOME}" ]

CMD "/usr/bin/sma-jinja-renderer" "${SMA_RENDERING_HOME}" "-f" "-r"
