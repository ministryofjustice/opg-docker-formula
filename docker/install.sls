include:
  - .repo


docker-pkg:
  pkg.installed:
    - name: lxc-docker-{{ default.get('docker:docker-version') }}
    - require:
      - pkgrepo: docker_repo


docker-py:
  pip.installed:
    - name: docker-py == {{ default.get('docker:py-version') }}
    - reload_modules: True
    - require:
      - pkg: docker-pkg


docker-compose-download:
  cmd.run:
    - name: "curl -L https://github.com/docker/compose/releases/download/{{ default.get('docker:docker-compose-version') }}/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose && chmod +x /usr/local/bin/docker-compose"
    - creates: /usr/local/bin/docker-compose


/etc/docker-compose:
  file.directory
