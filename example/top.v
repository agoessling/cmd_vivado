module top (input wire [3:0] btn,
            output wire [3:0] led);

  assign led[3:0] = btn[3:0];

endmodule
