.PHONY: status deploy backup apply-policy check-playbooks

status:
	python3 main/fabricctl/cli.py status

deploy:
	python3 main/fabricctl/cli.py deploy

backup:
	python3 main/fabricctl/cli.py backup

apply-policy:
	python3 main/fabricctl/cli.py apply-policy

check-playbooks:
	@for pb in scripts/ansible/playbooks/*.yml; do \
		ANSIBLE_CONFIG=scripts/ansible/ansible.cfg ansible-playbook -i scripts/ansible/inventories/production/hosts.yml "$$pb" --syntax-check; \
	done
