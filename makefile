run:
	python main.py

clean:
	rm *~ -f
	rm *pyc -f

#test view point translate
t_v:
	python test_viewpoint.py