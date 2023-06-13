#pragma once
#include "types.h"

#define MCH_SIZEOF_ARRAY(x)  (int)(sizeof((x))/sizeof((x)[0])) - 1
#define MCH_TO_ETERNITY_AND_BEYOND  while(true)

namespace Engine::Board
{
    const int_mch WIDTH  = 8; //* Number of horizontal board cells
    const int_mch HEIGHT = 8; //* Number of vertical board cells
    const coord_mch SIZE = WIDTH * HEIGHT; //* Total number of board cells
}