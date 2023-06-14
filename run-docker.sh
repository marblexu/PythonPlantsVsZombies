#bin/bash

RED='\033[0;31m'

GREEN='\033[0;32m'

NC='\033[0m' 

echo -e "${GREEN}Plants VS Zombies${NC}"

echo -e "${RED}Creating a container instance for the game...${NC}"

xhost + 

docker build -t sanmargparanjpe/plantsvszombie .

echo "${RED}Starting the instance...${NC}"

docker run -it --env="DISPLAY" --net=host  sanmargparanjpe/plantsvszombie  

echo "${RED}Quiting the Game${NC}"