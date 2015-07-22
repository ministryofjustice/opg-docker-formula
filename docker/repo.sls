docker_repo:
  pkgrepo.managed:
    - repo: 'deb https://get.docker.com/ubuntu docker main'
    - file: '/etc/apt/sources.list.d/docker.list'
    - key_url: salt://docker/files/docker.key
