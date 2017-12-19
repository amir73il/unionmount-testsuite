PKG_NAME = unionmount-testsuite
INSTALL = install
DESTDIR = /opt

all:
	@echo Nothing to do

clean:
	$(RM) *~ tests/*~

install:
	$(INSTALL) -m 755 -d $(DESTDIR)/$(PKG_NAME)
	$(INSTALL) -m 755 -d $(DESTDIR)/$(PKG_NAME)/tests
	$(INSTALL) -m 755 run $(DESTDIR)/$(PKG_NAME)
	$(INSTALL) -m 644 LICENCE.GPL README run *.py $(DESTDIR)/$(PKG_NAME)
	$(INSTALL) -m 644 tests/*.py $(DESTDIR)/$(PKG_NAME)/tests
