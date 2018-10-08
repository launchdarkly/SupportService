SITE_PACKAGES="lambda/lib/python3.6/site-packages"
DIR=$(pwd)

cd $SITE_PACKAGES
zip -r9 $DIR/LdLambda.zip *

cd $DIR
zip -g LdLambda.zip LdLambda.py