
PYTHON="$(shell which python3)"
PYS = image_rename.py
PYCS = $(PYS:.py=.pyc)

all: $(PYCS) test

test:
	+ $(PYTHON) -m unittest discover -v

%.pyc: %.py
	$(PYTHON) -m py_compile $<

clean:
	rm -f $(PYCS)

# end
