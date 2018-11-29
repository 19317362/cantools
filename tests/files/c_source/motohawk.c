/**
 * The MIT License (MIT)
 *
 * Copyright (c) 2018 Erik Moqvist
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associated documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use, copy,
 * modify, merge, publish, distribute, sublicense, and/or sell copies
 * of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

/**
 * This file was generated by cantools version 29.5.0 Thu Nov 29 20:08:59 2018.
 */

#include <string.h>

#include "motohawk.h"

#define UNUSED(x) (void)(x)

#define ftoi(value) (*((uint32_t *)(&(value))))
#define itof(value) (*((float *)(&(value))))
#define dtoi(value) (*((uint64_t *)(&(value))))
#define itod(value) (*((double *)(&(value))))

ssize_t motohawk_example_message_encode(
    uint8_t *dst_p,
    struct motohawk_example_message_t *src_p,
    size_t size)
{
    if (size < 8) {
        return (-EINVAL);
    }

    memset(&dst_p[0], 0, 8);

    dst_p[0] |= ((src_p->enable << 7) & 0x80);
    dst_p[0] |= ((src_p->average_radius << 1) & 0x7e);
    dst_p[0] |= ((src_p->temperature >> 11) & 0x01);
    dst_p[1] |= ((src_p->temperature >> 3) & 0xff);
    dst_p[2] |= ((src_p->temperature << 5) & 0xe0);

    return (8);
}

int motohawk_example_message_decode(
    struct motohawk_example_message_t *dst_p,
    uint8_t *src_p,
    size_t size)
{
    if (size < 8) {
        return (-EINVAL);
    }

    memset(dst_p, 0, sizeof(*dst_p));

    dst_p->enable |= ((uint8_t)(src_p[0] & 0x80) >> 7);
    dst_p->average_radius |= ((uint8_t)(src_p[0] & 0x7e) >> 1);
    dst_p->temperature |= ((uint16_t)(src_p[0] & 0x01) << 11);
    dst_p->temperature |= ((uint16_t)(src_p[1] & 0xff) << 3);
    dst_p->temperature |= ((uint16_t)(src_p[2] & 0xe0) >> 5);

    if (dst_p->temperature & (1 << 11)) {
        dst_p->temperature |= 0xf000;
    }

    return (0);
}

bool motohawk_example_message_enable_is_in_range(uint8_t value)
{
    UNUSED(value);

    return (true);
}

bool motohawk_example_message_average_radius_is_in_range(uint8_t value)
{
    return (value <= 50u);
}

bool motohawk_example_message_temperature_is_in_range(int16_t value)
{
    return ((value >= -2048) && (value <= 2047));
}
