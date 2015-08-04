{% from "docker/map.jinja" import docker with context %}

docker-compose-download:
  cmd.run:
    - name: "curl -L https://github.com/docker/compose/releases/download/{{ docker['docker-compose-version'] }}/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose"
    - creates: /usr/local/bin/docker-compose


/etc/docker-compose:
  file.directory
