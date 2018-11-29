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
 * This file was generated by cantools version 29.5.0 Thu Nov 29 20:06:28 2018.
 */

#ifndef MULTIPLEX_H
#define MULTIPLEX_H

#include <stdint.h>
#include <stdbool.h>
#include <unistd.h>

#ifndef EINVAL
#    define EINVAL -22
#endif

#define MULTIPLEX_MESSAGE1_FRAME_ID (0x123456u)



/**
 * Signals in message Message1.
 *
 * @param multiplexor Value as on the CAN bus.
 *            Defines data content for response messages.
 *            Range: -
 *            Scale: 1
 *            Offset: 0
 * @param bit_j Value as on the CAN bus.
 *            Range: -
 *            Scale: 1
 *            Offset: 0
 * @param bit_c Value as on the CAN bus.
 *            Range: -
 *            Scale: 1
 *            Offset: 0
 * @param bit_g Value as on the CAN bus.
 *            Range: -
 *            Scale: 1
 *            Offset: 0
 * @param bit_l Value as on the CAN bus.
 *            Range: -
 *            Scale: 1
 *            Offset: 0
 * @param bit_a Value as on the CAN bus.
 *            Range: -
 *            Scale: 1
 *            Offset: 0
 * @param bit_k Value as on the CAN bus.
 *            Range: -
 *            Scale: 1
 *            Offset: 0
 * @param bit_e Value as on the CAN bus.
 *            Range: -
 *            Scale: 1
 *            Offset: 0
 * @param bit_d Value as on the CAN bus.
 *            Range: -
 *            Scale: 1
 *            Offset: 0
 * @param bit_b Value as on the CAN bus.
 *            Range: -
 *            Scale: 1
 *            Offset: 0
 * @param bit_h Value as on the CAN bus.
 *            Range: -
 *            Scale: 1
 *            Offset: 0
 * @param bit_f Value as on the CAN bus.
 *            Range: -
 *            Scale: 1
 *            Offset: 0
 */
struct multiplex_message1_t {
    uint8_t multiplexor;
    uint8_t bit_j;
    uint8_t bit_c;
    uint8_t bit_g;
    uint8_t bit_l;
    uint8_t bit_a;
    uint8_t bit_k;
    uint8_t bit_e;
    uint8_t bit_d;
    uint8_t bit_b;
    uint8_t bit_h;
    uint8_t bit_f;
};

/**
 * Encode message Message1.
 *
 * @param[out] dst_p Buffer to encode the message into.
 * @param[in] src_p Data to encode.
 * @param[in] size Size of dst_p.
 *
 * @return Size of encoded data, or negative error code.
 */
ssize_t multiplex_message1_encode(
    uint8_t *dst_p,
    struct multiplex_message1_t *src_p,
    size_t size);

/**
 * Decode message Message1.
 *
 * @param[out] dst_p Object to decode the message into.
 * @param[in] src_p Message to decode.
 * @param[in] size Size of src_p.
 *
 * @return zero(0) or negative error code.
 */
int multiplex_message1_decode(
    struct multiplex_message1_t *dst_p,
    uint8_t *src_p,
    size_t size);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool multiplex_message1_multiplexor_is_in_range(uint8_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool multiplex_message1_bit_j_is_in_range(uint8_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool multiplex_message1_bit_c_is_in_range(uint8_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool multiplex_message1_bit_g_is_in_range(uint8_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool multiplex_message1_bit_l_is_in_range(uint8_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool multiplex_message1_bit_a_is_in_range(uint8_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool multiplex_message1_bit_k_is_in_range(uint8_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool multiplex_message1_bit_e_is_in_range(uint8_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool multiplex_message1_bit_d_is_in_range(uint8_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool multiplex_message1_bit_b_is_in_range(uint8_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool multiplex_message1_bit_h_is_in_range(uint8_t value);

/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool multiplex_message1_bit_f_is_in_range(uint8_t value);

#endif
