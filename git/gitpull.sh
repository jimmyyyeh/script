pull_submodule(){

  SUBMODULE_LOCATION=${CURRENT_LOCATION}/${SUBMODULE_PATH}
  SUBMODULE_HEAD=$(cat ${CURRENT_LOCATION}/.git/modules/$SUBMODULE_PATH/HEAD)
  SUBMODULE_BRANCH=$(echo $SUBMODULE_HEAD | awk -F'/' '{print $NF}')

  cd $SUBMODULE_LOCATION
  if [[ $SUBMODULE_BRANCH != ${DEV} ]]
  then
      git checkout $DEV
  fi
  echo "SUBMODULE: [${SUBMODULE_PATH}] BRANCH: [$SUBMODULE_BRANCH] -> [$DEV]"; git pull

  cd $CURRENT_LOCATION
}

DEV="develop"
CURRENT_LOCATION=$PWD
PROJECT_NAME=$(basename $PWD)
PROJECT_HEAD=$(cat $CURRENT_LOCATION/.git/HEAD)
PROJECT_BRANCH=$(echo $PROJECT_HEAD | awk -F'/' '{print $NF}')
SUBMODULE_PATH_STR=$(git config --file .gitmodules --get-regexp path | awk '{ print $2 }')
read -a SUBMODULE_PATH_LIST <<< $SUBMODULE_PATH_STR

### awk 'NR==1 {print $2}' limitation while the project has more than one submodules
#BRANCH=${1:-$PROJECT_NAME}
#SUBMODULE_NAME=$(echo $SUBMODULE_PATH | awk -F'/' '{print $NF}')

# pull current module
if [[ $PROJECT_BRANCH != $DEV ]]
then
    git checkout $DEV
fi
echo "PROJECT: [$PROJECT_NAME] | BRANCH: [$PROJECT_BRANCH] -> [$DEV]"; git pull

# pull submodule
for SUBMODULE_PATH in "${SUBMODULE_PATH_LIST[@]}"; do
    pull_submodule
done
