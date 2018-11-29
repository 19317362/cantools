from __future__ import print_function
import re
import time

from ...version import __version__


HEADER_FMT = '''\
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
 * This file was generated by cantools version {version} {date}.
 */

#ifndef {include_guard}
#define {include_guard}

#include <stdint.h>
#include <stdbool.h>
#include <unistd.h>

#ifndef EINVAL
#    define EINVAL -22
#endif

{frame_id_defines}

{choices_defines}

{structs}
{declarations}
#endif
'''

SOURCE_FMT = '''\
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
 * This file was generated by cantools version {version} {date}.
 */

#include <string.h>

#include "{header}"

#define UNUSED(x) (void)(x)

#define ftoi(value) (*((uint32_t *)(&(value))))
#define itof(value) (*((float *)(&(value))))
#define dtoi(value) (*((uint64_t *)(&(value))))
#define itod(value) (*((double *)(&(value))))

{definitions}\
'''

STRUCT_FMT = '''\
/**
 * Signals in message {database_message_name}.
 *
{comments}
 */
struct {database_name}_{message_name}_t {{
{members}
}};
'''

DECLARATION_FMT = '''\
/**
 * Encode message {database_message_name}.
 *
 * @param[out] dst_p Buffer to encode the message into.
 * @param[in] src_p Data to encode.
 * @param[in] size Size of dst_p.
 *
 * @return Size of encoded data, or negative error code.
 */
ssize_t {database_name}_{message_name}_encode(
    uint8_t *dst_p,
    struct {database_name}_{message_name}_t *src_p,
    size_t size);

/**
 * Decode message {database_message_name}.
 *
 * @param[out] dst_p Object to decode the message into.
 * @param[in] src_p Message to decode.
 * @param[in] size Size of src_p.
 *
 * @return zero(0) or negative error code.
 */
int {database_name}_{message_name}_decode(
    struct {database_name}_{message_name}_t *dst_p,
    uint8_t *src_p,
    size_t size);
'''

IS_IN_RANGE_DECLARATION_FMT = '''\
/**
 * Check that given signal is in allowed range.
 *
 * @param[in] value Signal to check.
 *
 * @return true if in range, false otherwise.
 */
bool {database_name}_{message_name}_{signal_name}_is_in_range({type_name} value);
'''

DEFINITION_FMT = '''\
ssize_t {database_name}_{message_name}_encode(
    uint8_t *dst_p,
    struct {database_name}_{message_name}_t *src_p,
    size_t size)
{{
{unused}\
{encode_variables}\
    if (size < {message_length}) {{
        return (-EINVAL);
    }}

    memset(&dst_p[0], 0, {message_length});
{encode_body}
    return ({message_length});
}}

int {database_name}_{message_name}_decode(
    struct {database_name}_{message_name}_t *dst_p,
    uint8_t *src_p,
    size_t size)
{{
{unused}\
{decode_variables}\
    if (size < {message_length}) {{
        return (-EINVAL);
    }}

    memset(dst_p, 0, sizeof(*dst_p));
{decode_body}
    return (0);
}}
'''

IS_IN_RANGE_DEFINITION_FMT = '''\
bool {database_name}_{message_name}_{signal_name}_is_in_range({type_name} value)
{{
{unused}\
    return ({check});
}}
'''

EMPTY_DEFINITION_FMT = '''\
ssize_t {database_name}_{message_name}_encode(
    uint8_t *dst_p,
    struct {database_name}_{message_name}_t *src_p,
    size_t size)
{{
    UNUSED(dst_p);
    UNUSED(src_p);
    UNUSED(size);

    return (0);
}}

int {database_name}_{message_name}_decode(
    struct {database_name}_{message_name}_t *dst_p,
    uint8_t *src_p,
    size_t size)
{{
    UNUSED(src_p);
    UNUSED(size);

    memset(dst_p, 0, sizeof(*dst_p));

    return (0);
}}
'''

SIGN_EXTENSION_FMT = '''
    if (dst_p->{name} & (1 << {shift})) {{
        dst_p->{name} |= {mask};
    }}

'''

SIGNAL_PARAM_COMMENT_FMT = '''\
 * @param {name} Value as on the CAN bus.
{comment}\
 *            Range: {range}
 *            Scale: {scale}
 *            Offset: {offset}\
'''


def _canonical(value):
    """Replace anything but 'a-z', 'A-Z', '0-9' and '_' with '_'.

    """

    return re.sub(r'\W', '_', value)


def _camel_to_snake_case(value):
    value = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', value)
    value = re.sub(r'(_+)', '_', value)
    value = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', value).lower()
    value = _canonical(value)

    return value


def _strip_blank_lines(lines):
    try:
        while lines[0] == '':
            lines = lines[1:]

        while lines[-1] == '':
            lines = lines[:-1]
    except IndexError:
        pass

    return lines


def _type_name(signal):
    type_name = None

    if signal.is_float:
        if signal.length == 32:
            type_name = 'float'
        elif signal.length == 64:
            type_name = 'double'
        else:
            print('warning: Floating point signal not 32 or 64 bits.')
    else:
        if signal.length <= 8:
            type_name = 'int8_t'
        elif signal.length <= 16:
            type_name = 'int16_t'
        elif signal.length <= 32:
            type_name = 'int32_t'
        elif signal.length <= 64:
            type_name = 'int64_t'
        else:
            print('warning: Signal lengths over 64 bits are not yet supported.')

        if type_name is not None:
            if not signal.is_signed:
                type_name = 'u' + type_name

    return type_name


def _get_type_suffix(type_name):
    try:
        return {
            'uint8_t': 'u',
            'uint16_t': 'u',
            'uint32_t': 'u',
            'int64_t': 'll',
            'uint64_t': 'ull',
            'float': 'f'
        }[type_name]
    except KeyError:
        return ''


def _get(value, default):
    if value is None:
        value = default

    return value


def _minimum_type_value(type_name):
    if type_name == 'int8_t':
        return -128
    elif type_name == 'int16_t':
        return -32768
    elif type_name == 'int32_t':
        return -2147483648
    elif type_name == 'int64_t':
        return -9223372036854775808
    elif type_name[0] == 'u':
        return 0
    else:
        return None


def _maximum_type_value(type_name):
    if type_name == 'int8_t':
        return 127
    elif type_name == 'int16_t':
        return 32767
    elif type_name == 'int32_t':
        return 2147483647
    elif type_name == 'int64_t':
        return 9223372036854775807
    elif type_name == 'uint8_t':
        return 255
    elif type_name == 'uint16_t':
        return 65535
    elif type_name == 'uint32_t':
        return 4294967295
    elif type_name == 'uint64_t':
        return 18446744073709551615
    else:
        return None


def _format_comment(comment):
    if comment:
        return '\n'.join([
            ' *            ' + line.rstrip()
            for line in comment.splitlines()
        ]) + '\n'
    else:
        return ''


def _format_decimal(value, is_float=False):
    if int(value) == value:
        value = int(value)

        if is_float:
            return str(value) + '.0'
        else:
            return str(value)
    else:
        return str(value)


def _format_range(signal):
    minimum = signal.decimal.minimum
    maximum = signal.decimal.maximum
    scale = signal.decimal.scale
    offset = signal.decimal.offset
    unit = _get(signal.unit, '-')

    if minimum is not None and maximum is not None:
        return '{}..{} ({}..{} {})'.format(
            _format_decimal((minimum - offset) / scale),
            _format_decimal((maximum - offset) / scale),
            minimum,
            maximum,
            unit)
    elif minimum is not None:
        return '{}.. ({}.. {})'.format(
            _format_decimal((minimum - offset) / scale),
            minimum,
            unit)
    elif maximum is not None:
        return '..{} (..{} {}'.format(
            _format_decimal((maximum - offset) / scale),
            maximum,
            unit)
    else:
        return '-'


def _generate_signal(signal):
    type_name = _type_name(signal)

    if type_name is None:
        return None, None

    name = _camel_to_snake_case(signal.name)
    comment = _format_comment(signal.comment)
    range_ = _format_range(signal)
    scale = _get(signal.scale, '-')
    offset = _get(signal.offset, '-')

    comment = SIGNAL_PARAM_COMMENT_FMT.format(name=name,
                                              comment=comment,
                                              range=range_,
                                              scale=scale,
                                              offset=offset)
    member = '    {} {};'.format(type_name, name)

    return comment, member


def _signal_segments(signal, invert_shift):
    index, pos = divmod(signal.start, 8)
    left = signal.length

    while left > 0:
        if signal.byte_order == 'big_endian':
            if left > (pos + 1):
                length = (pos + 1)
                pos = 7
                shift = -(left - length)
                mask = ((1 << length) - 1)
            else:
                length = left
                mask = ((1 << length) - 1)

                if (pos - length) >= 0:
                    shift = (pos - length + 1)
                else:
                    shift = (8 - left)

                mask <<= (pos - length + 1)
        else:
            if left >= (8 - pos):
                length = (8 - pos)
                shift = (left - signal.length) + pos
                mask = ((1 << length) - 1)
                mask <<= pos
                pos = 0
            else:
                length = left
                mask = ((1 << length) - 1)
                shift = pos
                mask <<= pos

        if invert_shift:
            if shift < 0:
                shift = '<< {}'.format(-shift)
            else:
                shift = '>> {}'.format(shift)
        else:
            if shift < 0:
                shift = '>> {}'.format(-shift)
            else:
                shift = '<< {}'.format(shift)

        yield index, shift, mask

        left -= length
        index += 1


def _format_encode_code_mux(message,
                            mux,
                            body_lines_per_index,
                            variable_lines,
                            conversion_lines):
    signal_name, multiplexed_signals = list(mux.items())[0]
    _format_encode_code_signal(message,
                               signal_name,
                               body_lines_per_index,
                               variable_lines,
                               conversion_lines)
    multiplexed_signals_per_id = sorted(list(multiplexed_signals.items()))
    signal_name = _camel_to_snake_case(signal_name)

    lines = [
        '',
        'switch (src_p->{}) {{'.format(signal_name)
    ]

    for multiplexer_id, multiplexed_signals in multiplexed_signals_per_id:
        body_lines = _format_encode_code_level(message,
                                               multiplexed_signals,
                                               variable_lines)
        lines.append('')
        lines.append('case {}:'.format(multiplexer_id))

        if body_lines:
            lines.extend(body_lines[1:-1])

        lines.append('    break;')

    lines.extend([
        '',
        'default:',
        '    break;',
        '}'])

    return [('    ' + line).rstrip() for line in lines]


def _format_encode_code_signal(message,
                               signal_name,
                               body_lines_per_index,
                               variable_lines,
                               conversion_lines):
    signal = message.get_signal_by_name(signal_name)
    signal_name = _camel_to_snake_case(signal_name)

    if signal.is_float:
        if signal.length == 32:
            variable = '    uint32_t {};'.format(signal_name)
            conversion = '    {0} = ftoi(src_p->{0});'.format(signal_name)
        else:
            variable = '    uint64_t {};'.format(signal_name)
            conversion = '    {0} = dtoi(src_p->{0});'.format(signal_name)

        variable_lines.append(variable)
        conversion_lines.append(conversion)

    for index, shift, mask in _signal_segments(signal, False):
        if index not in body_lines_per_index:
            body_lines_per_index[index] = []

        if signal.is_float:
            fmt = '    dst_p[{}] |= (({} {}) & 0x{:02x});'
        else:
            fmt = '    dst_p[{}] |= ((src_p->{} {}) & 0x{:02x});'

        line = fmt.format(index, signal_name, shift, mask)
        body_lines_per_index[index].append(line)


def _format_encode_code_level(message,
                              signal_names,
                              variable_lines):
    """Format one encode level in a signal tree.

    """

    body_lines_per_index = {}
    conversion_lines = []
    muxes_lines = []

    for signal_name in signal_names:
        if isinstance(signal_name, dict):
            mux_lines = _format_encode_code_mux(message,
                                                signal_name,
                                                body_lines_per_index,
                                                variable_lines,
                                                conversion_lines)
            muxes_lines += mux_lines
        else:
            _format_encode_code_signal(message,
                                       signal_name,
                                       body_lines_per_index,
                                       variable_lines,
                                       conversion_lines)

    body_lines = []

    for index in sorted(body_lines_per_index):
        body_lines += body_lines_per_index[index]

    if conversion_lines:
        conversion_lines += ['']

    body_lines = conversion_lines + body_lines + muxes_lines

    if body_lines:
        body_lines = [''] + body_lines + ['']

    return body_lines


def _format_encode_code(message):
    variable_lines = []
    body_lines = _format_encode_code_level(message,
                                           message.signal_tree,
                                           variable_lines)

    if variable_lines:
        variable_lines += ['', '']

    return '\n'.join(variable_lines), '\n'.join(body_lines)


def _format_decode_code_mux(message,
                            mux,
                            body_lines_per_index,
                            variable_lines,
                            conversion_lines):
    signal_name, multiplexed_signals = list(mux.items())[0]
    _format_decode_code_signal(message,
                               signal_name,
                               body_lines_per_index,
                               variable_lines,
                               conversion_lines)
    multiplexed_signals_per_id = sorted(list(multiplexed_signals.items()))
    signal_name = _camel_to_snake_case(signal_name)

    lines = [
        'switch (dst_p->{}) {{'.format(signal_name)
    ]

    for multiplexer_id, multiplexed_signals in multiplexed_signals_per_id:
        body_lines = _format_decode_code_level(message,
                                               multiplexed_signals,
                                               variable_lines)
        lines.append('')
        lines.append('case {}:'.format(multiplexer_id))
        lines.extend(_strip_blank_lines(body_lines))
        lines.append('    break;')

    lines.extend([
        '',
        'default:',
        '    break;',
        '}'])

    return [('    ' + line).rstrip() for line in lines]


def _format_decode_code_signal(message,
                               signal_name,
                               body_lines,
                               variable_lines,
                               conversion_lines):
    signal = message.get_signal_by_name(signal_name)
    signal_name = _camel_to_snake_case(signal_name)

    if signal.length <= 8:
        type_length = 8
    elif signal.length <= 16:
        type_length = 16
    elif signal.length <= 32:
        type_length = 32
    elif signal.length <= 64:
        type_length = 64

    for index, shift, mask in _signal_segments(signal, True):
        if signal.is_float:
            fmt = '    {} |= ((uint{}_t)(src_p[{}] & 0x{:02x}) {});'
        else:
            fmt = '    dst_p->{} |= ((uint{}_t)(src_p[{}] & 0x{:02x}) {});'

        line = fmt.format(signal_name, type_length, index, mask, shift)
        body_lines.append(line)

    if signal.is_float:
        if signal.length == 32:
            variable = '    uint32_t {} = 0;'.format(signal_name)
            line = '    dst_p->{0} = itof({0});'.format(signal_name)
        else:
            variable = '    uint64_t {} = 0;'.format(signal_name)
            line = '    dst_p->{0} = itod({0});'.format(signal_name)

        variable_lines.append(variable)
        conversion_lines.append(line)
    elif signal.is_signed:
        mask = ((1 << (type_length - signal.length)) - 1)

        if mask != 0:
            mask <<= signal.length
            formatted = SIGN_EXTENSION_FMT.format(name=signal_name,
                                                  shift=signal.length - 1,
                                                  mask=hex(mask))
            body_lines.extend(formatted.splitlines())


def _format_decode_code_level(message,
                              signal_names,
                              variable_lines):
    """Format one decode level in a signal tree.

    """

    body_lines = []
    conversion_lines = []
    muxes_lines = []

    for signal_name in signal_names:
        if isinstance(signal_name, dict):
            mux_lines = _format_decode_code_mux(message,
                                                signal_name,
                                                body_lines,
                                                variable_lines,
                                                conversion_lines)

            if muxes_lines:
                muxes_lines.append('')

            muxes_lines += mux_lines
        else:
            _format_decode_code_signal(message,
                                       signal_name,
                                       body_lines,
                                       variable_lines,
                                       conversion_lines)

    if conversion_lines:
        conversion_lines += ['']

    if body_lines:
        if body_lines[-1] != '':
            body_lines.append('')

    if muxes_lines:
        muxes_lines.append('')

    body_lines = body_lines + muxes_lines + conversion_lines

    if body_lines:
        body_lines = [''] + body_lines

    return body_lines


def _format_decode_code(message):
    variable_lines = []
    body_lines = _format_decode_code_level(message,
                                           message.signal_tree,
                                           variable_lines)

    if variable_lines:
        variable_lines += ['', '']

    return '\n'.join(variable_lines), '\n'.join(body_lines)


def _generate_struct(message):
    comments = []
    members = []

    for signal in message.signals:
        comment, member = _generate_signal(signal)

        if comment is not None:
            comments.append(comment)

        if member is not None:
            members.append(member)

    if not comments:
        comments = [' * @param dummy Dummy signal in empty message.']

    if not members:
        members = ['    uint8_t dummy;']

    return comments, members


def _unique_choices(choices):
    """Make duplicated choice names unique by first appending its value
    and then underscores until unique.

    """

    items = {
        value: _camel_to_snake_case(name).upper()
        for value, name in choices.items()
    }
    names = list(items.values())
    duplicated_names = [
        name
        for name in set(names)
        if names.count(name) > 1
    ]
    unique_choices = {
        value: name
        for value, name in items.items()
        if names.count(name) == 1
    }

    for value, name in items.items():
        if name in duplicated_names:
            name += _canonical('_{}'.format(value))

            while name in unique_choices.values():
                name += '_'

            unique_choices[value] = name

    return unique_choices


def _format_choices(signal, signal_name):
    choices = []

    for value, name in sorted(_unique_choices(signal.choices).items()):
        if signal.is_signed:
            fmt = '{signal_name}_{name}_CHOICE ({value})'
        else:
            fmt = '{signal_name}_{name}_CHOICE ({value}u)'

        choices.append(fmt.format(signal_name=signal_name.upper(),
                                  name=name,
                                  value=value))

    return choices


def _generate_is_in_range(message):
    """Generate range checks for all signals in given message.

    """

    signals = []

    for signal in message.signals:
        scale = signal.decimal.scale
        offset = (signal.decimal.offset / scale)
        minimum = signal.decimal.minimum
        maximum = signal.decimal.maximum

        if minimum is not None:
            minimum = (minimum / scale - offset)

        if maximum is not None:
            maximum = (maximum / scale - offset)

        type_name = _type_name(signal)
        suffix = _get_type_suffix(type_name)
        checks = []

        if minimum is not None:
            minimum_type_value = _minimum_type_value(type_name)

            if (minimum_type_value is None) or (minimum > minimum_type_value):
                minimum = _format_decimal(minimum, signal.is_float)
                checks.append('(value >= {}{})'.format(minimum, suffix))

        if maximum is not None:
            maximum_type_value = _maximum_type_value(type_name)

            if (maximum_type_value is None) or (maximum < maximum_type_value):
                maximum = _format_decimal(maximum, signal.is_float)
                checks.append('(value <= {}{})'.format(maximum, suffix))

        if not checks:
            checks = ['true']
        elif len(checks) == 1:
            checks = [checks[0][1:-1]]

        checks = ' && '.join(checks)

        signals.append((_camel_to_snake_case(signal.name),
                        type_name,
                        checks))

    return signals


def _generage_frame_id_defines(database_name, messages):
    return '\n'.join([
        '#define {}_{}_FRAME_ID (0x{:02x}u)'.format(
            database_name.upper(),
            _camel_to_snake_case(message.name).upper(),
            message.frame_id)
        for message in messages
    ])


def _generate_choices_defines(database_name, messages):
    choices_defines = []

    for message in messages:
        message_name = _camel_to_snake_case(message.name)

        for signal in message.signals:
            if signal.choices is None:
                continue

            signal_name = _camel_to_snake_case(signal.name)
            choices = _format_choices(signal, signal_name)
            signal_choices_defines = '\n'.join([
                '#define {}_{}_{}'.format(database_name.upper(),
                                          message_name.upper(),
                                          choice)
                for choice in choices
            ])
            choices_defines.append(signal_choices_defines)

    return '\n\n'.join(choices_defines)


def _generate_structs(database_name, messages):
    structs = []

    for message in messages:
        comments, members = _generate_struct(message)
        structs.append(
            STRUCT_FMT.format(database_message_name=message.name,
                              message_name=_camel_to_snake_case(message.name),
                              database_name=database_name,
                              comments='\n'.join(comments),
                              members='\n'.join(members)))

    return '\n'.join(structs)


def _generate_declarations(database_name, messages):
    declarations = []

    for message in messages:
        message_name = _camel_to_snake_case(message.name)
        is_in_range_declarations = []

        for signal_name, type_name, _ in _generate_is_in_range(message):
            is_in_range_declaration = IS_IN_RANGE_DECLARATION_FMT.format(
                database_name=database_name,
                message_name=message_name,
                signal_name=signal_name,
                type_name=type_name)
            is_in_range_declarations.append(is_in_range_declaration)

        declaration = DECLARATION_FMT.format(database_name=database_name,
                                             database_message_name=message.name,
                                             message_name=message_name)
        declaration += '\n' + '\n'.join(is_in_range_declarations)
        declarations.append(declaration)

    return '\n'.join(declarations)


def _generate_definitions(database_name, messages):
    definitions = []

    for message in messages:
        message_name = _camel_to_snake_case(message.name)
        is_in_range_definitions = []

        for signal_name, type_name, check in _generate_is_in_range(message):
            if check == 'true':
                unused = '    UNUSED(value);\n\n'
            else:
                unused = ''

            is_in_range_definition = IS_IN_RANGE_DEFINITION_FMT.format(
                database_name=database_name,
                message_name=message_name,
                signal_name=signal_name,
                type_name=type_name,
                unused=unused,
                check=check)
            is_in_range_definitions.append(is_in_range_definition)

        if message.length > 0:
            encode_variables, encode_body = _format_encode_code(message)
            decode_variables, decode_body = _format_decode_code(message)

            if encode_body:
                unused = ''
            else:
                unused = '    UNUSED(src_p);\n\n'

            definition = DEFINITION_FMT.format(database_name=database_name,
                                               database_message_name=message.name,
                                               message_name=message_name,
                                               message_length=message.length,
                                               unused=unused,
                                               encode_variables=encode_variables,
                                               encode_body=encode_body,
                                               decode_variables=decode_variables,
                                               decode_body=decode_body)
        else:
            definition = EMPTY_DEFINITION_FMT.format(database_name=database_name,
                                                     message_name=message_name)

        definition += '\n' + '\n'.join(is_in_range_definitions)
        definitions.append(definition)

    return '\n'.join(definitions)


def generate(database, database_name, header_name):
    """Generate C source code from given CAN database `database`.

    `database_name` is used as a prefix for all defines, data
    structures and functions.

    `header_name` is the file name of the C header file, which is
    included by the C source file.

    This function returns a tuple of the C header and source files as
    strings.

    """

    date = time.ctime()
    messages = database.messages
    include_guard = '{}_H'.format(database_name.upper())
    frame_id_defines = _generage_frame_id_defines(database_name, messages)
    choices_defines = _generate_choices_defines(database_name, messages)
    structs = _generate_structs(database_name, messages)
    declarations = _generate_declarations(database_name, messages)
    definitions = _generate_definitions(database_name, messages)

    header = HEADER_FMT.format(version=__version__,
                               date=date,
                               include_guard=include_guard,
                               frame_id_defines=frame_id_defines,
                               choices_defines=choices_defines,
                               structs=structs,
                               declarations=declarations)

    source = SOURCE_FMT.format(version=__version__,
                               date=date,
                               header=header_name,
                               definitions=definitions)

    return header, source
