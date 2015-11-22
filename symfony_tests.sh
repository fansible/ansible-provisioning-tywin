
APPDIR=/var/tests
SYMFONYTESTDIR=`pwd`/testsymfony

mkdir $SYMFONYTESTDIR
cp test/composer.json $SYMFONYTESTDIR
cd $SYMFONYTESTDIR && yes | python ../generate.py && cd -
rm $SYMFONYTESTDIR/devops/provisioning/vars/main.yml
cp test/main.yml $SYMFONYTESTDIR/devops/provisioning/vars/

RUNNER=`sudo docker run -dit -v $SYMFONYTESTDIR:$APPDIR -w $APPDIR maximethoonsen/ubuntu-trusty-ansible`

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

rm -rf $SYMFONYTESTDIR
