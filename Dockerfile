FROM python:2.7-alpine3.7

RUN mkdir -p /root/apt
WORKDIR /root/apt

# Update
RUN apk update && apk upgrade

RUN echo "http://dl-4.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
RUN apk --update add --no-cache \
    lapack-dev \
    gcc \
    freetype-dev \
    git

# Download gambit source and gurobi
RUN git clone https://github.com/gambitproject/gambit.git
RUN cd gambit && git checkout 700a9d746942ecd9453d9af33c4d7f73478a0dc4

RUN wget http://packages.gurobi.com/7.5/gurobi7.5.2_linux64.tar.gz

RUN tar -xzf gurobi7.5.2_linux64.tar.gz
RUN mv /root/apt/gurobi752 /opt
RUN rm gurobi7.5.2_linux64.tar.gz

RUN apk add automake libtool intltool build-base autoconf libpng py-setuptools gfortran

RUN pip install numpy==1.14.1

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# install gambit
WORKDIR /root/apt/gambit
RUN aclocal
RUN libtoolize
RUN automake --add-missing
RUN autoconf
RUN ./configure --disable-enumpoly
RUN make
RUN make install
RUN cd src/python && python setup.py install

# install gurobi vars
ENV GUROBI_HOME="/opt/gurobi752/linux64"
ENV PATH="${PATH}:${GUROBI_HOME}/bin"
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${GUROBI_HOME}/lib"

RUN mkdir /opt/gurobi752 && mv /opt/linux64 /opt/gurobi752/linux64
RUN cd /opt/gurobi752/linux64 && python setup.py install