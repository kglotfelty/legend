
ROOT = /data/lenin2/Scripts/MyStuff/ciao46/ciao-4.6/contrib
DEST = lib/python2.7/site-packages/chips_contrib
DEV  = /data/da/Docs/scripts/dev


CP_F = /bin/cp -fv

RDIR = $(ROOT)/$(DEST)
DDIR = $(DEV)/$(DEST)


PYCODE = legend.py


all: $(PYCODE)

install: all
	@mkdir -p $(RDIR)
	@$(CP_F) $(PYCODE) $(RDIR)/

install-dev: all
	@mkdir -p $(DDIR)
	@$(CP_F) $(PYCODE) $(DDIR)/

