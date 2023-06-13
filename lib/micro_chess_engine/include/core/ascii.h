#pragma once
#include "types.h"

namespace Engine::ASCII
{
    enum Bits : char
    {
        NOCASE    = 0b00011111,  //* Unique ASCII letter bits
        LOWERCASE = 0b00100000,  //* Bit that indicates if letter is lowercase
        MSCB      = 0b01000000   //* Most Significant Char Bit
    };

    /* Convert char to lower case */
    constexpr char to_lower(const char letter) { return letter | LOWERCASE;    }
    /* Convert char to upper case */
    constexpr char to_upper(const char letter) { return letter & (~LOWERCASE); }

    /* Encode nocase letter into uint_mch */
    constexpr uint_mch encode(const char value) { return (uint_mch)value & NOCASE; }
    /* Decode nocase letter from uint_mch */
    constexpr char     decode(const uint_mch value) { return encode(value) | MSCB;     }
}