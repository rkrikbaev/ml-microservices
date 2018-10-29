FROM ubuntu:xenial

# enable utf-8 locale
ENV PYTHONUNBUFFERED 1

ADD install.sh /tmp/install.sh
RUN sh -e /tmp/install.sh

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8

#RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
#    python3 get-pip.py && \
#    rm get-pip.py

# must be installed before scikit-learn
#RUN pip3 install numpy>=1.11.0
#RUN pip3 install scipy>=0.17.0

#ADD requirements.txt /tmp/requirements.txt
#RUN pip3 install -r /tmp/requirements.txt

# create flask as service
ADD post-install.sh /opt/script-server/src/script-server/post-install.sh
RUN /bin/bash /opt/script-server/src/script-server/post-install.sh

#RUN pip3 install --upgrade git+git://github.com/lefant/hyperopt.git
#RUN pip3 install git+git://github.com/msmbuilder/osprey.git
# settle for lightfm 1.8 via requirements.txt for now
#RUN pip3 install git+git://github.com/lyst/lightfm.git

ADD run.sh /
RUN chmod +x /run.sh
EXPOSE 5003
CMD ["/run.sh"]
