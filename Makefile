build:
	docker build --rm -t ausome-foods:latest .

run:
	docker run --rm -it -v `pwd`:/home ausome-foods:latest /bin/ash
