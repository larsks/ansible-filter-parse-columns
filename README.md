# parse_columns filter for Ansible

Recent versions of Ansible include the [parse_cli][] module, which uses regular expression to parse output from network devices into structured data. Many switch commands produce columnar data, and while it's possible to parse this with regular expressions it can be unnecessarily complicated (especially in situations in which some rows may have empty values for some columns).

This repository includes the `parse_columns` module, designed to parse columnar data. Like the `parse_cli` data, `parse_columns` reads column descriptions from a YAML file. You might use it like this:

```
- hosts: switches
  gather_facts: false
  tasks:
    - name: get port information
      cli_command:
        command: show port all
      register: show_port_all

    - name: parse show port all output
      set_fact:
        ports: >-
          {{
            show_port_all.stdout |
            parse_columns('cols/show_port_all.yml')
          }}

    - name: show some information
      debug:
        msg: >-
          port {{ item.interface }} is {{ item.link_status }}{%
          if item.phys_status %} at {{ item.phys_status }}{% endif %}
      loop: "{{ ports }}"
      loop_control:
        label: "{{ item.interface }}"
```

Which might produce output like:

```
TASK [show some information] *********************************************************
ok: [office-sw-0] => (item=0/1) => {
    "msg": "port 0/1 is Down"
}
ok: [office-sw-0] => (item=0/2) => {
    "msg": "port 0/2 is Up at 1000 Full"
}
ok: [office-sw-0] => (item=0/3) => {
    "msg": "port 0/3 is Down"
}
...
```
