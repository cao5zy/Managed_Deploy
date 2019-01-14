- name: "deploy {{'{{'}}auth_db{{'}}'}}"
  docker_container:
    name: "{{'{{'}}auth_db{{'}}'}}"
    image: "mongo:4.0"
    state: started
    exposed: "{{'{{'}}auth_db_port{{'}}'}}"
    entrypoint: "mongod --port={{'{{'}}auth_db_port{{'}}'}} --bind_ip=0.0.0.0"
  register: auth_db_result

- debug: var=auth_db_result.ansible_facts.docker_container.NetworkSettings.IPAddress

- set_fact:
    auth_db_ip: "{{'{{'}} auth_db_result.ansible_facts.docker_container.NetworkSettings.IPAddress {{'}}'}}"

- debug: var=auth_db_ip