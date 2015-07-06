cd no-generation/badcomposer && python ../../../generate.py && cd -
cd no-generation/no-composer-no-package && python ../../../generate.py && cd -
cd symfony/complete && python ../../../generate.py && rm -rf devops && rm ansible.cfg && rm Vagrantfile  && cd -
