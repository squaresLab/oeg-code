FROM ckinneer/apt-buildenv:1.0

WORKDIR /root/apt
COPY startup.sh /root/apt

RUN mkdir /opt/gurobi
COPY gurobi.lic /opt/gurobi/

ENTRYPOINT ["/root/apt/startup.sh"]