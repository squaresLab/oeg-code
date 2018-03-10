FROM ckinneer/apt-buildenv:1.0

WORKDIR /root/apt
COPY startup.sh /root/apt

ENTRYPOINT ["/root/apt/startup.sh"]
