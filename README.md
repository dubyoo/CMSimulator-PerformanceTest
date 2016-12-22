# CMSimulator-PerformanceTest



CMSimulator Features
	1. CMSimulator can create multiple SGs, each SG can create multiple CMs(each CM has different MAC), each CM can create multiple STBs(each STB in a CM has different IP).
	2. Support configurable items includes SBSS IP/Port, SGID, CCP rate, number of CMs per SG, number of STBs per CM, and Mcast IP segment.
	4. Support to separately run/stop each SG.
	5. Each SG send RTSP CCP join/leave request to a random channel from random CM and STB.


Guide
	1. Configuration
		Add SG configuration in "./conf/SGConfig.xml"

	2. Run Simulator
		a. start
			$ ./bin/CMSimulator.sh start 100 101
			Successfully to start 100
			Successfully to start 101
	
		b. status
			$ ./bin/CMSimulator.sh status
			root  7835  1  0 02:05 pts/2  00:00:00 python sendtosg.py 100
			root  7847  1  0 02:05 pts/2  00:00:00 python sendtosg.py 101
	
		c. stop
			stop sg:
				$ ./bin/CMSimulator.sh stop 100 101
				Successfully to stop 100
				Successfully to stop 101
			stop all:
				$ ./bin/CMSimulator.sh stop all
				Successfully to stop all

	3. Log
		If you start simulator with "./CMSimulator.sh start 100"
		Log info will be saved in "./log/100.log"

	4. Other
		a. Send one CCP request message:
			$ ./bin/senddte.py
			USAGE : senddte.py [IP] [Port] [SGID] [MAC] [stb_ip] [group_ip] [leave_or_join]
			SAMPLE: senddte.py 10.90.242.246 20000 801 00-1C-26-C8-5C-50 192.168.1.1 238.1.1.1 join

		b. Compile and Install Python:
		  download Python-2.7.11.tgz
			$ tar -zxvf Python-2.7.11.tgz
			$ cd Python-2.7.11
			$ ./configure
			$ make
			$ make install
