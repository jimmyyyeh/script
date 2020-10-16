:<<!
instructions for use
-> cd ./projcet_path
-> full_path/exec_screen.sh [-p] (title1 entrypoint1.py) (title2 entrypoint2.py)....

example
-> sh -p ~./exec_screen.sh title01 app.py # git pull before execute
-> sh ~./exec_screen.sh title01 app.py # don't do git pull before execute
!
# 指定screen和container名稱
SCREEN_NAME=${PWD##*/}
CONTAINER_NAME=$SCREEN_NAME
# 指定專案路徑
PROJECT_PATH=${PWD}
# 依序指定 window title/ container 指令 (依序 兩兩一對)
ARGS=("$@")
# determine if execute git pull before docker-compose up
if [ "${ARGS[0]}" == -p ]; then
    COMMANDS=("gitpullall" "docker-compose down;docker-compose up")
    INPUT_COMMANDS="${ARGS[@]:1}"
    INPUT_COMMANDS=($INPUT_COMMANDS)
else
    COMMANDS=("" "docker-compose down;docker-compose up")
    INPUT_COMMANDS=("${ARGS[@]}")
fi
COMMAND_LEN=${#COMMANDS[@]}
CONTAINER_SIZE=$CONTAINER_SIZE+$COMMAND_LEN
# 指定對應元素專案要開幾個window
INPUT_COMMAND_SIZE=${#INPUT_COMMANDS[@]}
CONTAINER_SIZE=$(($INPUT_COMMAND_SIZE / 2))
# 分離title和command
WINDOW_TITLES=()
CONTAINER_COMMANDS=()
for ((n=0; n<$INPUT_COMMAND_SIZE; n+=2)); do
    WINDOW_TITLES+=("${INPUT_COMMANDS[$n]}")
    CONTAINER_COMMANDS+=("${INPUT_COMMANDS[$n+1]}")
done
echo CREATE SCREEN WITH "$(($CONTAINER_SIZE + 2))" WINDDOWS IN "$PROJECT_PATH"


create_screen_window(){
  # create window with screen command
  if (( "$(($1))" >= 2 ));
  then
      screen -x -S $SCREEN_NAME -p $1 -X stuff "${COMMANDS[$1]}"
      screen -x -S $SCREEN_NAME -p $1 -X stuff $'\n'
      screen -x -S $SCREEN_NAME -p $1 -X stuff "python3 ${CONTAINER_COMMANDS[$1-2]}"
      screen -x -S $SCREEN_NAME -p $1 -X stuff $'\n'
  else
      screen -x -S $SCREEN_NAME -p $1 -X stuff "${COMMANDS[$1]}"
      screen -x -S $SCREEN_NAME -p $1 -X stuff $'\n'
  fi
  # create new window before exit
  if (( "$(($1))" >= 1 ))  && (( $(($1)) < $(($COMMAND_LEN-1)) ));
  then
    screen -S $SCREEN_NAME -X screen -t "${WINDOW_TITLES[$1-1]}"
  elif (( "$(($1))" < 1 )) && (( $(($1)) < $(($COMMAND_LEN-1)) ));
  then
    screen -S $SCREEN_NAME -X screen 
  fi
  
  if (( "$(($1))" <= 1 ));
  then
    sleep 3
  else
    sleep 0
  fi
  echo EXECUTE COMMAND: "${COMMANDS[$1]}" SUCCESSFUL!
}

# create new screen with detatched mode
screen -dmS $SCREEN_NAME
echo "${SCREEN_NAME} WAS CREATED!"

for ((n=0; n<$CONTAINER_SIZE; n++)); do
  COMMANDS+=("docker exec -it ${CONTAINER_NAME} bash")
done
COMMAND_LEN=${#COMMANDS[@]}
for ((n=0; n<$COMMAND_LEN; n++)); do
  create_screen_window $n
done

# https://unix.stackexchange.com/questions/287165/is-there-a-way-to-create-a-screen-windows-from-shell-script
# https://blog.csdn.net/u011606714/article/details/53471532

