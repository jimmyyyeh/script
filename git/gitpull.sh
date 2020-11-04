pull_submodule(){

  SUBMODULE_LOCATION=${PROJECT_PATH}/${SUBMODULE_PATH}
  SUBMODULE_HEAD=$(cat ${PROJECT_PATH}/.git/modules/$SUBMODULE_PATH/HEAD)
  SUBMODULE_BRANCH=$(echo $SUBMODULE_HEAD | awk -F'/' '{print $NF}')

  cd $SUBMODULE_LOCATION
  if [[ $SUBMODULE_BRANCH != ${BRANCH} ]]
  then
      git checkout $BRANCH
  fi
  echo "SUBMODULE: [${SUBMODULE_PATH}] BRANCH: [$SUBMODULE_BRANCH] -> [$BRANCH]"; git pull

  cd $PROJECT_PATH
}

set_args(){
  # get project root path and project name
  PROJECT_PATH=$(git rev-parse --show-toplevel)
  PROJECT_NAME=$(basename ${PROJECT_PATH})

  # get current branch
  PROJECT_HEAD=$(cat ${PROJECT_PATH}/.git/HEAD)
  CURRENT_BRANCH=$(echo $PROJECT_HEAD | awk -F'/' '{print $NF}')

  # get branch
  if [ -z $1 ];
    then
      BRANCH="develop"
  else
      BRANCH=$1
  fi

  # check if submodule already init
  submodules="`cat ${PROJECT_PATH}/.git/config | grep submodule`"

    if [ -z "$submodules" ];
      then
        INIT_SUBMODULE=true
    else
        INIT_SUBMODULE=false
    fi
}

init_project(){
  if [[ $CURRENT_BRANCH != $BRANCH ]]
  then
      git checkout $BRANCH
  fi
  echo "PROJECT: [$PROJECT_NAME] | BRANCH: [$CURRENT_BRANCH] -> [$BRANCH]"; git pull

  # init submodule
  if [ $INIT_SUBMODULE = true ]
    then
      git submodule update --init --recursive
      echo [SUBMODULE INIT FINISHED]
  fi

  # read submodule
  SUBMODULE_PATH_STR=$(git config --file .gitmodules --get-regexp path | awk '{ print $2 }')
  read -a SUBMODULE_PATH_LIST <<< $SUBMODULE_PATH_STR
}


set_args $1
init_project


# pull submodule
for SUBMODULE_PATH in "${SUBMODULE_PATH_LIST[@]}"; do
    pull_submodule
done
