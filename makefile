NAME_NO_JIT=revelation_nojit_linux64
NAME_WITH_JIT=revelation_jit_linux64

PYPY=pypy
RPYTHON=./rpython

build_no_jit:
	$(PYPY) $(RPYTHON) --output $(NAME_NO_JIT) main.py

build_with_jit:
	$(PYPY) $(RPYTHON) --output $(NAME_WITH_JIT) -O jit main.py

clean:
	rm $(NAME_NO_JIT)
