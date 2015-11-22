
APPDIR=/var/tests
NODETESTDIR=`pwd`/testnode

mkdir $NODETESTDIR
cp test/package.json $NODETESTDIR
cd $NODETESTDIR && yes | python ../generate.py && cd -
rm $NODETESTDIR/devops/provisioning/vars/main.yml
cp test/main.yml $NODETESTDIR/devops/provisioning/vars/

RUNNER=`sudo docker run -dit -v $NODETESTDIR:$APPDIR -w $APPDIR maximethoonsen/ubuntu-trusty-ansible`

assert () {
    docker exec -it $RUNNER $1 || ( echo ${2-'Test is failed'} && exit 1 )
}

{
    assert "ansible --version"   &&
    assert "ansible-playbook -c local devops/provisioning/playbook.yml  --syntax-check"
    # assert "ansible-playbook -c local devops/provisioning/playbook.yml"                  &&
    # assert "ansible-playbook -c local devops/provisioning/playbook.yml" | grep changed=0 &&

    # assert "which node"
    # assert "which npm"

} || {

    echo "Tests are failed"

}

docker stop $RUNNER

rm -rf $NODETESTDIR
