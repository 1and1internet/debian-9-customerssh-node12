FROM 1and1internet/debian-9
MAINTAINER brian.wilkinson@1and1.co.uk
COPY files/ /

RUN export DEBIAN_FRONTEND=noninteractive DEBCONF_NONINTERACTIVE_SEEN=true && \
  apt-get update && \
  echo "root:*:18022:0:99999:7:::" >> /etc/shadow && \
  apt-get install -y curl apt-transport-https ca-certificates lsb-release gnupg \
  		openssh-client openssh-sftp-server git vim traceroute \
		telnet nano dnsutils wget iputils-ping mysql-client libmariadbclient-dev && \
  curl -sL https://deb.nodesource.com/setup_12.x | bash - && \
  apt-get install -y nodejs && \
  apt-get autoremove -y && apt-get autoclean -y && \
  chmod 0777 /var/www && \
  rm -rf /usr/src/tmp/ && \
  rm -f /etc/ssh/ssh_host_* && \
  chmod -R 0777 /etc/supervisor/conf.d && \
  sed -i '/^root/d' /etc/shadow

ENV HOME=/var/www
WORKDIR /var/www

# Install and configure the cron service
ENV EDITOR=/usr/bin/vim \
	CRON_LOG_FILE=/var/spool/cron/cron.log \
	CRON_LOCK_FILE=/var/spool/cron/cron.lock \
	CRON_ARGS=""
RUN \
  apt-get update && apt-get install -y -o Dpkg::Options::="--force-confold" \
  	build-essential logrotate man && \
  cd /src/cron-3.0pl1 && \
  make install && \
  mkdir -p /var/spool/cron/crontabs && \
  chmod -R 777 /var/spool/cron && \
  cp debian/crontab.main /etc/crontab && \
  cd - && \
  rm -rf /src && \
  find /etc/cron.* -type f | egrep -v 'logrotate|placeholder' | xargs -i rm -f {} && \
  chmod 666 /etc/logrotate.conf && \
  chmod -R 777 /var/lib/logrotate && \
  apt-get remove build-essential && \
  apt-get autoremove -y && apt-get autoclean -y && \
  rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["/bin/bash", "/init/entrypoint"]
CMD ["/init/supervisord"]
