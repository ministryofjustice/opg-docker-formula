{% from "docker/map.jinja" import docker with context %}

include:
  - .repo


docker-pkg:
  pkg.installed:
    - name: lxc-docker-{{ docker['docker-version'] }}
    - require:
      - pkgrepo: docker_repo


docker-py:
  pip.installed:
    - name: docker-py == {{ docker['docker-py-version'] }}
    - reload_modules: True
    - require:
      - pkg: docker-pkg

