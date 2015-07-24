/root/.dockercfg:
  file.managed:
    - source: salt://docker/templates/dockercfg
    - mode: 0600
    - user: root
    - group: root
    - template: jinja


/etc/default/docker:
  file.managed:
    - template: jinja
    - source: salt://docker/templates/docker/default
    - watch_in:
      - service: docker


docker:
  service.running:
    - require:
      - pkg: docker-pkg
