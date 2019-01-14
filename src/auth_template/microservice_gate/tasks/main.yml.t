---

- name: init login service deploy folder
  file:
    path: "{{'{{'}}microservice_gate_root{{'}}'}}"
    state: directory

- name: init logs folder 
  file:
    path: "{{'{{'}}microservice_gate_root{{'}}'}}/logs"
    state: directory

- name: init conf folder 
  file:
    path: "{{'{{'}}microservice_gate_root{{'}}'}}/conf.d"
    state: directory

- name: configure nginx
  template:
    src: login.conf.template
    dest: "{{'{{'}}microservice_gate_root{{'}}'}}/conf.d/login.conf"

- name: deploy the nginx server
  docker_container:
    name: "{{'{{'}}microservice_gate{{'}}'}}"
    image: "{{'{{'}}microservice_gate_image_name{{'}}'}}:{{'{{'}}microservice_gate_image_git_version{{'}}'}}"
    ports:
      - "{{'{{'}}public_port{{'}}'}}:{{'{{'}}public_port{{'}}'}}"
    restart: yes
    volumes:
      - "{{'{{'}}microservice_gate_root{{'}}'}}/logs:/usr/local/openresty/nginx/logs:Z"
      - "{{'{{'}}microservice_gate_root{{'}}'}}/conf.d:/usr/local/openresty/nginx/conf.d:Z"



...