# cmd_vivado

This package provides a mechanism for interacting with the [Xilinx Vivado
IDE](https://www.xilinx.com/products/design-tools/vivado.html) through a
simplified command line tool.  Vivado provides a Tcl based interface to
programatically avoid the GUI, but it is too low level to directly interact with
a build system.  This package provides an interface suitable to be used with
build tools such as [Make](https://www.gnu.org/software/make/manual/make.html).

## Usage

`cmd_vivado` works by running the Vivado IDE in Tcl mode as a server
(`vivado_server.py`).  This is advantageous as Vivado takes several (~8 on my
current machine) seconds to start up.  The client (`vivado_client.py`) provides
a simplified command line interface to the synthesize, place, route, and program
workflow.  The client communicates to the server through sockets.  Theoretically
the server could run remotely from the client, although this has not been
tested.

### Server

```Shell
./vivado_server.py --exec_path=~/VivadoPath/bin/vivado
```

### Client

```Shell
./vivado_client.py command --options
```

The client currently implements the following commands:
* `synth` - Synthesize a design.
* `place` - Place a synthesized design.
* `route` - Route a placed design.
* `bitstream` - Write a `.bit` bitstream.
* `cfg_mem` - Write a `.bin` configuration memory file.
* `load` - Load a bitstream onto a device.
* `flash` - Flash a configuration onto on-board flash.

Further information can be sought with the `--help` option.

### Make

```Shell
make all
```

The provided `Makefile` shows how to combine `cmd_vivado` with a build tool for
a rudimentary workflow.  Verbosity can be increased with `make VERBOSE=1`.

## Example Project

The `example` directory contains the simplest possible project that demonstrates
`cmd_vivado` use with a `Makefile`.  It is targeted at the [Digilent Arty A7
A35T](https://reference.digilentinc.com/reference/programmable-logic/arty-a7/start)
development board.

### Steps

1. Install [Vivado](https://www.xilinx.com/support/download.html) including
   drivers (requires an extra step on Linux).
2. Plug in the Arty A7 micro USB.
2. Start the server with `./vivado_server.py exec_path=VIVADO_PATH`.  Make sure
   to change `VIVADO_PATH` with path to your Vivado installation.
3. From the `example` directory run `make VERBOSE=1 flash`.
4. Wait for Vivado to do it's thing.
5. Play with the buttons (`BTN[3:0]`) and observe LEDS (`LED[7:4]`).

## Status

Currently `cmd_vivado` has only the features required for the simplest
demonstration.  I expect many features will need to be added for it to be useful
in non-trivial projects, but hopefully this framework will provide a good
starting point.  I am learning about FPGAs as I go, and I welcome suggestions.

### Wish List

* Explore ways to speed up various parts of workflow.
* Explore Out Of Context (OOC) workflow and how it could be leveraged for
  incremental compilation.
