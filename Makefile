NAME := DSLR

PACKAGE =	matplotlib\
			numpy\
			pandas\
			scikit-learn\
			seaborn\

install:
	@python3 -m pip install $(PACKAGE)

.PHONY: install