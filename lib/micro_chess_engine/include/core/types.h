#pragma once
#include <stdint.h>

#define MCH_INT_BITS 8

using int_mch   = int8_t;   //* General use signed 8-bit integer
using uint_mch  = uint8_t;  //* General use unsigned 8-bit integer
const int_mch   INT_MCH_MAX   = INT8_MAX;
const uint_mch  UINT_MCH_MAX  = UINT8_MAX;

using coord_mch = int_mch;  //* Board coordinate values
using pce_mch   = uint_mch; //* Piece describing type (individual pieces themselves, their props, etc.)
const coord_mch COORD_MCH_MAX = INT_MCH_MAX;
const pce_mch   PCE_MCH_MAX   = UINT_MCH_MAX;

const uint_mch LEFTMOST_BIT = 1 << (MCH_INT_BITS - 1);