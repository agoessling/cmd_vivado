NAME = # Name of project. Used for bitstream naming.

PART = # Target part number. 'get_parts' shows valid options.
CFGMEM = # Configuration memory part number. 'get_hw_cfgmems' shows valid options.
CFGMEMSIZE = # Configuration memory size in MB.
CFGMEMINTERFACE = # Configuration memory interface. e.g. SPIx4

SRCS = # List of verilog sources.
TOP = # Top level verilog module.
IOXDS = # List of constraint files placement.
BITXDS = # List of constraint files for bitstream generation.

VIV = # Path to vivado_client.py.
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
