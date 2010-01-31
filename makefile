run:
	python main.py -d

clean:
	rm *~ -f
	rm *pyc -f

#test view point translate
t_v:
	python test_viewpoint.py
#test opengl
t_gl:
	python test_opengl.py
#test animation
t_a:
	python test_animation.py