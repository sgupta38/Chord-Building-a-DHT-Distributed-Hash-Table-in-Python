#!/bin/bash

echo "Please enter a test to check."
echo "     1. WriteFile"
echo "     2. ReadFile"
echo "     3. FindSucc"
echo "     4. FindPred"
echo "     5. getNodeSucc"

read input_variable

case $input_variable in
    1) 
		cat node.txt | sed -e "s/:/ /" | while read ip port
        do
 			 ./unit_tests/write_client.sh $ip $port
		done

        ;;
    2) 
		cat node.txt | sed -e "s/:/ /" | while read ip port
        do
 			 ./unit_tests/read_client.sh $ip $port
		done

        ;;
    3) 
 		cat node.txt | sed -e "s/:/ /" | while read ip port
        do
 			 ./unit_tests/fs_client.sh $ip $port
		done

        ;;
    4) 
		cat node.txt | sed -e "s/:/ /" | while read ip port
        do
 			 ./unit_tests/fp_client.sh $ip $port
		done
		;;
	5)
		cat node.txt | sed -e "s/:/ /" | while read ip port
        do
 			 ./unit_tests/getNodeSucc_client.sh $ip $port
		done
        ;;
    *) # anything else
        echo "not recognised" 
        ;;
esac