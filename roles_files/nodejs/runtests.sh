#!/bin/sh

APPDIR=/var/tests
CURDIR=`pwd`

RUNNER=`docker run -v $CURDIR:$APPDIR -w $APPDIR -dit ansible/ubuntu14.04-ansible bash`

assert () {
    docker exec -it $RUNNER $1 || ( echo ${2-'Test is failed'} && exit 1 )
}

{
    assert "ansible-playbook -c local --syntax-check test-src.yml"   &&
    assert "ansible-playbook -c local test-src.yml"                  &&
    assert "ansible-playbook -c local test-src.yml" | grep changed=0 &&

    assert "which node"
    assert "which npm"

} || {

    echo "Tests are failed"

}

docker stop $RUNNER
