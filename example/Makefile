NAME = arty

PART = xc7a35ticsg324-1l
CFGMEM = mt25ql128-spi-x1_x2_x4
CFGMEMSIZE = 16
CFGMEMINTERFACE = SPIx4

SRCS = top.v
TOP = top
IOXDS = io_constraints.xdc
BITXDS = bitstream_constraints.xdc

VIV = ../vivado_client.py
OBJDIR = obj
TARGET = $(OBJDIR)/$(NAME)
$(shell mkdir -p $(OBJDIR))

COMMON = -p $(PART)
ifeq ($(VERBOSE), 1)  # Verbosity can be added with 'make VERBOSE=1'
  COMMON += --verbose
endif

.PHONY: all
all: $(TARGET).bit

$(OBJDIR)/post_synth.dcp: $(SRCS)
	$(VIV) synth $(COMMON) -t $(TOP) -v $(SRCS) -o $@

$(OBJDIR)/post_place.dcp: $(OBJDIR)/post_synth.dcp $(IOXDS)
	$(VIV) place $(COMMON) -c $(IOXDS) -i $< -o $@

$(OBJDIR)/post_route.dcp: $(OBJDIR)/post_place.dcp
	$(VIV) route $(COMMON) -i $< -o $@

$(TARGET).bit: $(OBJDIR)/post_route.dcp $(BITXDS)
	$(VIV) bitstream $(COMMON) -c $(BITXDS) -i $< -o $@

$(TARGET).bin: $(TARGET).bit
	$(VIV) cfg_mem $(COMMON) --size $(CFGMEMSIZE) --interface $(CFGMEMINTERFACE) -i $< -o $@

.PHONY: load
load: $(TARGET).bit
	$(VIV) load $(COMMON) -i $<

.PHONY: flash
flash: $(TARGET).bin
	$(VIV) flash $(COMMON) --memory $(CFGMEM) -i $<

.PHONY: clean
clean:
	rm -f $(OBJDIR)/*
