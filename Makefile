install:
	pip install -r requirements.txt
	cp main.py /usr/main.py
	cp config.json /usr/config.json
	cp README.md /usr/README.md
	cp requirements.txt /usr/requirements.txt

	cd /usr/
	mkdir kurisu
	mv main.py /kurisu/main.py
	mv config.json /kurisu/config.json
	mv README.md /kurisu/README.md
	mv requirements.txt /kurisu/requirements.txt
	echo "python3 /usr/kurisu/main.py" > /usr/bin/kurisu
	chmod +x /usr/bin/kurisu
