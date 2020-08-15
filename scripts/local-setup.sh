#!/bin/bash

red=$(printf '\033[0;31m')
green=$(printf '\033[0;32m')
blue=$(printf '\033[34m')
white=$(printf '\033[97m')
bold=$(printf '\033[1m')
cl=$(printf '\033[0m')

cat << EOF
        ________________________________________________________
       /                                                       /
      /     ______            __      ____  ___               /
     /     /_  __/___  ____  / /____ / __ \\/ (_)___          /
    /       / / / __ \\/ __ \\/ / ___// / / / / / __ \\        /
   /       / / / /_/ / /_/ / (__  )/ /_/ / / / / / /       /
  /       /_/  \\____/\\____/_/____(_)____/_/_/_/ /_/       /
 /                                                       /
/_______________________________________________________/

EOF

printf "\n%s  Running checks...%s\n" $bold $cl

printf "%s    Docker:%s" $blue $cl
type docker > /dev/null 2>&1
if [ "$?" != "0" ]
then
  printf " %sMissing%s\n" $red $cl
  printf "    -----------------------------\n"
  printf "    Install docker:\n"

cat << EOF

      $ ${bold}${green}sudo apt update${cl}

      $ ${bold}${green}curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -${cl}

      # This assumes you are running Ubuntu 18.04
      $ ${bold}${green}sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"${cl}

      $ ${bold}${green}sudo apt update${cl}

      $ ${bold}${green}sudo apt install docker-ce${cl}

      $ ${bold}${green}sudo usermod -aG docker ${USER}${cl}

      $ ${bold}${green}su - ${USER}${cl}

EOF
  exit 1
else
  printf " %sFound version %s%s%s\n" $green $white $(docker version -f "{{ .Server.Version }}") $cl
fi



printf "%s    Docker Compose:%s" $blue $cl
type docker-compose > /dev/null 2>&1
if [ "$?" != "0" ]
then
  printf " %sMissing%s\n" $red $cl
  printf "    -----------------------------\n"
  printf "    Install docker-compose:\n"

cat << EOF

      $ $bold$green sudo curl -L "https://github.com/docker/compose/releases/download/1.26.2/docker-compose-\$(uname -s)-\$(uname -m)" -o /usr/local/bin/docker-compose $cl

      $ $bold$green sudo chmod +x /usr/local/bin/docker-compose $cl

EOF

  exit 1
else
  printf " %sFound version %s%s%s\n" $green $white $(docker-compose version --short) $cl
fi


function bullet () {
  printf "  * $1"
}

printf "\n%s  ------------------------------- %s\n" $bold $cl
printf "  ${bold}Useful commands:${cl}\n\n"
bullet "${green}docker-compose pull${cl}:    Pull the latest images\n"
bullet "${green}docker-compose build${cl}:   Build the latest images\n"
bullet "${green}${bold}docker-compose up -d${cl}:   Run all the services ${blue}<-- Run this one!${cl}\n\n"

printf "  ${blue}After exec-ing into the backend container (${bold}docker exec -ti tools-backend bash${cl}${blue})${cl}\n"
bullet "${green}nox${cl}:                          Run all test/lint sessions\n"
bullet "${green}pytest -svra tests/ --cov${cl}:    Run unittests\n"
printf "\n"
