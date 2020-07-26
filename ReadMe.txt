Team member1 : Kenilkumar Maheshkumar Patel (1001765579)
Team member2 : Parth Mukeshbhai Navadia (1001778479)

----------------------------------------------------------------------------------------

Developement Language : Python 
Block chain : Komodo

----------------------------------------------------------------------------------------

Setting up the block chain 

----------------------------------------------------------------------------------------

On system1 

./komodod -ac_name=coins -ac_supply=20000 -addnode=<Ip address of second system>&

----------------------------------------------------------------------------------------

On system2 

./komodod -ac_name=coins -ac_supply=20000 -addnode=<Ip address of first system>&

----------------------------------------------------------------------------------------

Start mining on any of the system

./komodo-cli -ac_name=coins setgenerate true $(nproc)

----------------------------------------------------------------------------------------

Generate new address and pubkey on both system and keep note of it

newaddress=$(./komodo-cli -ac_name=coins getnewaddress)
pubkey=$(./komodo-cli -ac_name=coins validateaddress $newaddress | jq -r '.pubkey' )
./komodo-cli -ac_name=coins setpubkey $pubkey

----------------------------------------------------------------------------------------

Initially send some coins to system which have 0 coins

./komodo-cli -ac_name=coins sendtoaddress <reciepent address> 1000

----------------------------------------------------------------------------------------

Now start the dealer first and then player and keep playing game

python dealer.py

python player.py

----------------------------------------------------------------------------------------

Note : After pressing play button for the first time don't just keep pressing that button wait for 10-20 seconds to confirm the balance and got reflected on GUI

----------------------------------------------------------------------------------------