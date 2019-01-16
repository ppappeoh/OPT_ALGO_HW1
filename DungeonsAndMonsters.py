from pwn import *
import Queue
import time
mazePos = [
     200,  206,  210,  214,  218,  224,  228,  232,  236,  242,  248,  252,  256,  260,  266,  270, 
     404,  408,  414,  420,  424,  430,  434,  438,  444,  450,  454,  460,  464,  470,  474,  480, 
     644,  650,  656,  660,  666,  670,  674,  678,  684,  688,  692,  698,  702,  706,  712,  718, 
     876,  882,  886,  892,  896,  902,  906,  910,  916,  920,  924,  928,  934,  940,  946,  950, 
    1102, 1108, 1114, 1118, 1124, 1130, 1136, 1142, 1148, 1152, 1158, 1162, 1168, 1172, 1178, 1182, 
    1316, 1320, 1326, 1330, 1336, 1342, 1348, 1354, 1358, 1364, 1370, 1374, 1380, 1386, 1390, 1396, 
    1542, 1548, 1552, 1558, 1562, 1568, 1572, 1578, 1582, 1588, 1592, 1598, 1604, 1610, 1616, 1622, 
    1762, 1768, 1772, 1778, 1782, 1786, 1792, 1796, 1802, 1806, 1810, 1816, 1820, 1826, 1830, 1836, 
    2006, 2010, 2014, 2018, 2022, 2028, 2032, 2038, 2044, 2048, 2054, 2060, 2064, 2070, 2074, 2078, 
    2236, 2240, 2244, 2250, 2254, 2258, 2264, 2268, 2272, 2278, 2284, 2288, 2294, 2300, 2304, 2308, 
    2472, 2478, 2482, 2486, 2492, 2496, 2500, 2506, 2510, 2516, 2522, 2526, 2532, 2536, 2540, 2546, 
    2698, 2702, 2708, 2714, 2720, 2726, 2730, 2734, 2740, 2746, 2750, 2754, 2758, 2764, 2770, 2774, 
    2938, 2944, 2948, 2954, 2960, 2966, 2970, 2976, 2980, 2984, 2988, 2994, 3000, 3006, 3010, 3014, 
    3154, 3160, 3166, 3170, 3176, 3182, 3188, 3192, 3198, 3204, 3210, 3216, 3222, 3228, 3232, 3236, 
    3376, 3382, 3386, 3390, 3394, 3400, 3404, 3410, 3414, 3420, 3426, 3430, 3436, 3440, 3446, 3452, 
    3616, 3620, 3624, 3628, 3632, 3636, 3640, 3644, 3650, 3656, 3660, 3664, 3668, 3672, 3676, 3680, 
    ]
mazeDir = [
    [ 0, 1, 0, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 1, 1, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 1, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 1, 1, 0, ],
    [ 0, 1, 0, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 1, 1, 1, ],
    [ 0, 1, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 1, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 0, 0, 0, 1, ],
    [ 1, 1, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 0, 1, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 0, 1, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 1, 1, 1, ],
    [ 0, 1, 1, 0, ],
    [ 0, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 1, 1, 0, ],
    [ 0, 0, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 1, 0, 1, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 0, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 0, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 0, 1, 0, 0, ],
    [ 0, 1, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 1, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 0, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 1, 0, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 1, 1, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 1, 0, 1, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 0, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 0, 0, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 0, 1, 0, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 1, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 1, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 0, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 1, 0, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 0, 0, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 1, 1, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 1, 0, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 0, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 1, 1, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 0, 1, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 0, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 0, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 0, 1, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 1, 1, 1, ],
    [ 0, 1, 1, 0, ],
    [ 0, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 0, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 0, 0, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 0, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 0, 1, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 1, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 0, 1, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 1, 1, 0, ],
    [ 0, 1, 0, 1, ],
    [ 1, 1, 1, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 0, 0, 1, ],
    [ 1, 0, 1, 0, ],
    [ 0, 1, 0, 0, ],
    [ 1, 1, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 0, 1, 1, ],
    [ 1, 0, 1, 1, ],
    [ 1, 0, 1, 0, ],
    [ 1, 0, 0, 0, ],
    [ 1, 0, 0, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 0, 1, 1, ],
    [ 0, 0, 1, 1, ],
    [ 1, 0, 1, 1, ],
    [ 1, 0, 1, 0, ],
    ];
moveOff = [-16, 16, -1, 1];
def mpos2Pos(mp):
	return mazePos.index(mp)

def bfs (pos, monster):
	path_queue = Queue.Queue()
	pos_queue = Queue.Queue()
	visit = [0]*260

	pos_queue.put(pos)
	path_queue.put([])

	while(not(pos_queue.empty())):
		now_pos = pos_queue.get()
		now_path = path_queue.get()
		visit[now_pos] = 1

		for direction in range(0, 4, 1):
			if(mazeDir[now_pos][direction] == 0):
				continue
			newpos = now_pos + moveOff[direction]
			new_path = now_path + [direction]
			if(visit[newpos] == 1):
				continue
			if(newpos == monster):
				return 1, new_path
			pos_queue.put(newpos)		
			path_queue.put(new_path)


		

commands = "wsadefq"
	


r = remote("edu-ctf.zoolab.org", 6666)


r.sendline("abc") #name
r.recvuntil('x\n')
state = "initial_find"
game_map = r.recvuntil("[>] action: ", drop=True)
player_mpos = game_map.find("O")
monster_mpos = game_map.find("M")
if(player_mpos == -1):
	player_mpos = game_map.find("B")
	monster_mpos = player_mpos
	state="attack"
attack_pos = mpos2Pos(player_mpos)
player_pos = mpos2Pos(player_mpos)
monster_pos = mpos2Pos(monster_mpos)
attack_time = 0


while(1):
	print(attack_time)
	if(attack_time >= 100):
		break
	if(state == "find"):

		monster_mpos = game_map.find("M")
		monster_pos = mpos2Pos(monster_mpos)
		player_mpos = game_map.find("G")
		player_pos = mpos2Pos(player_mpos)

		res, path = bfs(player_pos, monster_pos)

		if(len(path) >= 5):
			for i in range(0, len(path) - 3, 1):
				r.sendline(commands[path[i]])
				print("command1 " + commands[path[i]])
				print(r.recvuntil("[>] action: ", drop=True))
				#absorbmap=r.recvuntil("[>] action: ", drop=True)
			for i in range(len(path) - 4, -1, -1):
				r.sendline(commands[path[i] ^ 1])
				print("command2 " + commands[path[i]^1])
				print(r.recvuntil("[>] action: ", drop=True))
				#absorbmap=r.recvuntil("[>] action: ", drop=True)
			print("attack!")	
			state = "attack"	

		elif(len(path) == 4):
			r.sendline("e")
			print(r.recvuntil("[>] action: ", drop=True))
			#absorbmap=r.recvuntil("[>] action: ", drop=True)
			r.sendline(commands[path[0]])
			player_pos = player_pos + moveOff[path[0]]
			print(r.recvuntil("[>] action: ", drop=True))
			#absorbmap=r.recvuntil("[>] action: ", drop=True)

			r.sendline(commands[path[1]])
			player_pos = player_pos + moveOff[path[1]]
			print(r.recvuntil("[>] action: ", drop=True))
			#absorbmap=r.recvuntil("[>] action: ", drop=True)

			r.sendline("f")
			pre_map = r.recvuntil("x\n", drop=True)
			game_map = r.recvuntil("[>] action: ", drop=True)
			print(pre_map + game_map)
			attack_time = attack_time + 1


		elif(len(path) == 2):
			r.sendline("e")
			print(r.recvuntil("[>] action: ", drop=True))
			#absorbmap=r.recvuntil("[>] action: ", drop=True)

			r.sendline(commands[path[0]])
			player_pos = player_pos + moveOff[path[0]]
			print(r.recvuntil("[>] action: ", drop=True))
			#absorbmap=r.recvuntil("[>] action: ", drop=True)

			r.sendline("f")
			pre_map = r.recvuntil("x\n", drop=True)
			game_map = r.recvuntil("[>] action: ", drop=True)
			print(pre_map + game_map)
			attack_time = attack_time + 1

		elif(len(path) == 3):
			r.sendline(commands[path[0]])
			player_pos = player_pos + moveOff[path[0]]
			print(r.recvuntil("[>] action: ", drop=True))
			#absorbmap=r.recvuntil("[>] action: ", drop=True)

			r.sendline(commands[path[0] ^ 1])
			player_pos = player_pos + moveOff[path[0] ^ 1]
			print(r.recvuntil("[>] action: ", drop=True))
			#absorbmap=r.recvuntil("[>] action: ", drop=True)

			state = "attack"	

		elif(len(path) == 1):
			state = "attack"

	elif(state == "attack"):

		print("eat")
		r.sendline("e")
		print(r.recvuntil("[>] action: ", drop=True))
		#absorbmap=r.recvuntil("[>] action: ", drop=True)

		r.sendline("f")
		pre_map = r.recvuntil("x\n", drop=True)
		game_map = r.recvuntil("[>] action: ", drop=True)
		print(pre_map + game_map)
		attack_time = attack_time + 1
		state = "find"

		
	if(state == "initial_find"):
		res, path = bfs(player_pos, monster_pos)
		if(len(path) >= 5):
			for i in range(0, len(path) - 2, 1):
				r.sendline(commands[path[i]])
				print(r.recvuntil("[>] action: ", drop=True))
				#absorbmap=r.recvuntil("[>] action: ", drop=True)

			r.sendline("f")
			pre_map = r.recvuntil("x\n", drop=True)
			game_map = r.recvuntil("[>] action: ", drop=True)
			print(pre_map + game_map)
			attack_time = attack_time + 1

		elif(len(path) == 4):

			r.sendline(commands[path[0]])
			player_pos = player_pos + moveOff[path[0]]
			print(r.recvuntil("[>] action: ", drop=True))
			#absorbmap=r.recvuntil("[>] action: ", drop=True)

			r.sendline(commands[path[1]])
			player_pos = player_pos + moveOff[path[1]]
			print(r.recvuntil("[>] action: ", drop=True))
			#absorbmap=r.recvuntil("[>] action: ", drop=True)

			r.sendline("f")
			pre_map = r.recvuntil("x\n", drop=True)
			game_map = r.recvuntil("[>] action: ", drop=True)
			print(pre_map + game_map)
			attack_time = attack_time + 1

		elif(len(path) == 2):

			r.sendline(commands[path[0]])
			player_pos = player_pos + moveOff[path[0]]
			print(r.recvuntil("[>] action: ", drop=True))
			#absorbmap=r.recvuntil("[>] action: ", drop=True)

			r.sendline("f")
			pre_map = r.recvuntil("x\n", drop=True)
			game_map = r.recvuntil("[>] action: ", drop=True)
			print(pre_map + game_map)
			attack_time = attack_time + 1

		elif(len(path) == 3):
			r.sendline(commands[path[0]])
			player_pos = player_pos + moveOff[path[0]]
			print(r.recvuntil("[>] action: ", drop=True))
			#absorbmap=r.recvuntil("[>] action: ", drop=True)

			r.sendline(commands[path[1]])
			player_pos = player_pos + moveOff[path[1]]
			print(r.recvuntil("[>] action: ", drop=True))
			#absorbmap=r.recvuntil("[>] action: ", drop=True)

			r.sendline("f")	
			pre_map = r.recvuntil("x\n", drop=True)
			game_map = r.recvuntil("[>] action: ", drop=True)
			print(pre_map + game_map)
			attack_time = attack_time + 1

		elif(len(path) == 1):
			r.sendline(commands[path[0]])
			player_pos = player_pos + moveOff[path[0]]
			print(r.recvuntil("[>] action: ", drop=True))
			#absorbmap=r.recvuntil("[>] action: ", drop=True)

			r.sendline("f")	
			pre_map = r.recvuntil("x\n", drop=True)
			game_map = r.recvuntil("[>] action: ", drop=True)
			print(pre_map + game_map)
			attack_time = attack_time + 1
		state = "find"



